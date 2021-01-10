import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
LOG_DATA = config.get('S3', 'LOG_DATA')
SONG_DATA = config.get('S3', 'SONG_DATA')
LOG_JSONPATH = config.get('S3', 'LOG_JSONPATH') 
ARN = config.get('IAM_ROLE', 'ARN')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = " DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
	CREATE TABLE IF NOT EXISTS staging_events(
		event_id BIGINT IDENTITY(0,1) NOT NULL,
		artist VARCHAR,
		auth VARCHAR,
		first_name VARCHAR,
		gender  VARCHAR,
		item_session VARCHAR,
		last_name VARCHAR,
		length FLOAT,
		level VARCHAR,
		location VARCHAR,
		method VARCHAR,
		page VARCHAR,
		registration FLOAT,
		session_id INT NOT NULL SORTKEY DISTKEY,
		song VARCHAR,
		status INT,
		ts BIGINT,
		user_agent VARCHAR,
		user_id INT
		);
""")

staging_songs_table_create = ("""
	CREATE TABLE IF NOT EXISTS staging_songs (
	num_songs INT,
	artist_id VARCHAR NOT NULL SORTKEY DISTKEY,
	artist_latitude VARCHAR,
	artist_longitude VARCHAR,
	artist_location VARCHAR,
	artist_name VARCHAR,
	song_id VARCHAR NOT NULL,
	title VARCHAR,
	duration FLOAT,
	year INT
	);
""")

songplay_table_create = ("""
	CREATE TABLE IF NOT EXISTS songplays(
	songplay_id INT IDENTITY(0,1) NOT NULL SORTKEY,
	start_time TIMESTAMP NOT NULL,
	user_id VARCHAR NOT NULL DISTKEY,
	level VARCHAR(10) NOT NULL,
	song_id VARCHAR NOT NULL,
	artist_id VARCHAR NOT NULL,
	session_id INT NOT NULL,
	location VARCHAR,
	user_agent VARCHAR NOT NULL
	);
""")

user_table_create = ("""
	CREATE TABLE IF NOT EXISTS users(
	user_id VARCHAR NOT NULL SORTKEY,
	first_name VARCHAR NOT NULL,
	last_name VARCHAR NOT NULL,
	gender VARCHAR,
	level VARCHAR NOT NULL
	)
	diststyle all;
	
""")

song_table_create = ("""
	CREATE TABLE IF NOT EXISTS songs(
	song_id VARCHAR NOT NULL SORTKEY,
	title VARCHAR,
	artist_id VARCHAR NOT NULL,
	year INT NOT NULL,
	duration NUMERIC NOT NULL
	) 
	diststyle all;
""")

artist_table_create = ("""
	CREATE TABLE IF NOT EXISTS artists(
	artist_id VARCHAR NOT NULL SORTKEY,
	name VARCHAR NOT NULL,
	location VARCHAR,
	latitude VARCHAR,
	longitude VARCHAR
	)
	diststyle all;
""")

time_table_create = ("""
	CREATE TABLE IF NOT EXISTS time (
	start_time TIMESTAMP NOT NULL SORTKEY,
	hour INT,
	day INT,
	week INT,
	month INT,
	year INT,
	weekday INT
	)
	diststyle all;
""")

# STAGING TABLES

staging_events_copy = ("""
	COPY staging_events FROM '{}' 
	IAM_ROLE '{}'
    FORMAT AS JSON '{}'
    region 'us-west-2';
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
	COPY staging_songs FROM '{}'
	IAM_ROLE '{}'
	FORMAT AS JSON 'auto'
    region 'us-west-2';
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (
	start_time,
	user_id,
	level,
	song_id,
	artist_id,
	session_id,
	location,
	user_agent
)
SELECT DISTINCT 
TIMESTAMP 'epoch' + se.ts/1000* INTERVAL '1 second' as start_time,
se.user_id,
se.level,
ss.song_id,
ss.artist_id,
se.session_id,
se.location,
se.user_agent
FROM staging_events se
JOIN staging_songs ss
ON se.song = ss.title
where se.page = 'NextSong';

""")

user_table_insert = ("""
INSERT INTO users (
	user_id,
	first_name,
	last_name,
	gender,
	level
	)
SELECT DISTINCT
	user_id,
	first_name,
	last_name,
	gender,
	level
FROM staging_events 
WHERE page = 'NextSong';
""")

song_table_insert = ("""
INSERT INTO songs (
song_id,
title,
artist_id,
year,
duration
	)
SELECT DISTINCT
song_id,
title,
artist_id,
year,
duration
FROM staging_songs;

""")

artist_table_insert = ("""
INSERT INTO artists (
artist_id,
name,
location,
latitude,
longitude)
SELECT DISTINCT
artist_id,
artist_name as name,
artist_location as location,
artist_latitude as latitude,
artist_longitude as longitude
FROM staging_songs;
""")

time_table_insert = ("""
INSERT INTO time (
start_time,
hour,
day,
week,
month,
year,
weekday
)
SELECT DISTINCT
TIMESTAMP 'epoch' + ts/1000* INTERVAL '1 second' as start_time,
EXTRACT(hour FROM start_time) as hour,
EXTRACT(day FROM start_time) as day,
EXTRACT(week FROM start_time) as week,
EXTRACT(month FROM start_time) as month,
EXTRACT(year FROM start_time) as year,
EXTRACT(dow FROM start_time) as weekday
FROM staging_events 
WHERE page = 'NextSong';
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
