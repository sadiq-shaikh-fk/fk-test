import asyncpg
from app.config import Config

db_pool = None

async def create_db_pool():
    global db_pool
    db_pool = await asyncpg.create_pool(
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        host=Config.DB_HOST,
        min_size=10,
        max_size=50,
        command_timeout=60
    )

async def insert_channel_data(data):
    async with db_pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO youtube_channels (channel_id, title, description, view_count, subscriber_count, video_count, published_at, thumbnail_high_url, country, privacy_status, made_for_kids, image_banner_url, upload_playlist_id)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
            ON CONFLICT (channel_id) DO NOTHING
        ''', data['yt_channel_id'], data['channel_title'], data['channel_desc'], data['channel_view_count'], 
            data['channel_subscriber_count'], data['channel_video_count'], data['channel_published_at'], 
            data['channel_thumbnail_high_url'], data['channel_country'], data['channel_privacy_status'], 
            data['channel_made_for_kids'], data['channel_image_banner_url'], data['channel_upload_playlist_id'])

async def insert_video_data(video_ids):
    batch_size = 100
    async with db_pool.acquire() as connection:
        for i in range(0, len(video_ids), batch_size):
            batch = video_ids[i:i + batch_size]
            await connection.executemany('''
                INSERT INTO youtube_videos (video_id)
                VALUES ($1)
                ON CONFLICT (video_id) DO NOTHING
            ''', [(video_id,) for video_id in batch])
