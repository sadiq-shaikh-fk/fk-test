from googleapiclient.discovery import build
from app.config import Config
import asyncio

api_keys = Config.API_KEYS
current_key_index = 0
request_count = 0
max_requests_per_key = 1000

async def get_youtube_service():
    global current_key_index, request_count
    if request_count >= max_requests_per_key:
        current_key_index = (current_key_index + 1) % len(api_keys)
        request_count = 0
    youtube = build('youtube', 'v3', developerKey=api_keys[current_key_index])
    request_count += 1
    return youtube

async def get_channel_details_from_id(channel_id):
    youtube = await get_youtube_service()
    request = youtube.channels().list(
        part="snippet,statistics,brandingSettings,contentDetails,status",
        id=channel_id,
        fields="items(id,snippet(title,description,publishedAt,thumbnails(high),localized,country),"
               "statistics(viewCount,subscriberCount,videoCount),"
               "brandingSettings(image,channel),contentDetails(relatedPlaylists(uploads)),"
               "status(privacyStatus,madeForKids)"
    )
    try:
        response = request.execute()
        details = response['items'][0]
        return {
            'yt_channel_id': details['id'],
            'channel_title': details['snippet']['title'],
            'channel_desc': details['snippet']['description'],
            'channel_published_at': details['snippet']['publishedAt'],
            'channel_thumbnail_high_url': details['snippet']['thumbnails']['high']['url'],
            'channel_country': details['snippet'].get('country', None),
            'channel_view_count': details['statistics'].get('viewCount', 0),
            'channel_subscriber_count': details['statistics'].get('subscriberCount', 0),
            'channel_video_count': details['statistics'].get('videoCount', 0),
            'channel_privacy_status': details['status'].get('privacyStatus', None),
            'channel_made_for_kids': details['status'].get('madeForKids', None),
            'channel_image_banner_url': details['brandingSettings']['image'].get('bannerExternalUrl', None),
            'channel_upload_playlist_id': details['contentDetails']['relatedPlaylists'].get('uploads', None)
        }
    except Exception as e:
        raise e

async def get_video_id_from_playlist(playlist_id, pageToken=None):
    youtube = await get_youtube_service()
    request = youtube.playlistItems().list(
        part="snippet,contentDetails,status",
        playlistId=playlist_id,
        pageToken=pageToken,
        maxResults=50
    )
    try:
        response = request.execute()
        video_ids = [item['contentDetails']['videoId'] for item in response.get('items', [])]
        return {
            'video_ids': video_ids,
            'nextPageToken': response.get('nextPageToken')
        }
    except Exception as e:
        raise e
