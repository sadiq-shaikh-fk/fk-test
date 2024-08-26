from app.api_functions import get_channel_details_from_id, get_video_id_from_playlist
from app.database import insert_channel_data, insert_video_data
from app import celery
from app.logging_config import setup_logging
import pybreaker

logger = setup_logging()
circuit_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)

@celery.task(bind=True)
async def fetch_and_store_channel_data(self, channel_id):
    logger.info(f"Task started for channel ID: {channel_id}")
    try:
        details = await circuit_breaker.call_async(get_channel_details_from_id, channel_id)
        await insert_channel_data(details)
        logger.info(f"Task completed for channel ID: {channel_id}")
    except pybreaker.CircuitBreakerError as e:
        logger.error(f"Circuit breaker open for channel ID: {channel_id}. Retrying...")
        self.retry(exc=e, countdown=60)
    except Exception as e:
        logger.error(f"Error in task for channel ID: {channel_id} - {str(e)}")
        self.retry(exc=e, countdown=60)

@celery.task(bind=True)
async def process_playlist(self, playlist_id):
    logger.info(f"Task started for playlist ID: {playlist_id}")
    pageToken = None
    try:
        while True:
            data = await circuit_breaker.call_async(get_video_id_from_playlist, playlist_id, pageToken)
            video_ids = data.get('video_ids', [])
            await insert_video_data(video_ids)

            pageToken = data.get('nextPageToken')
            if not pageToken:
                break
        logger.info(f"Task completed for playlist ID: {playlist_id}")
    except pybreaker.CircuitBreakerError as e:
        logger.error(f"Circuit breaker open for playlist ID: {playlist_id}. Retrying...")
        self.retry(exc=e, countdown=60)
    except Exception as e:
        logger.error(f"Error in task for playlist ID: {playlist_id} - {str(e)}")
        self.retry(exc=e, countdown=60)
