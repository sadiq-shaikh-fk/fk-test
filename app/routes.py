from quart import jsonify
from app.tasks import fetch_and_store_channel_data, process_playlist
from app import app

@app.route('/channel/<string:channel_id>', methods=['GET'])
async def get_channel_details(channel_id):
    # Enqueue the task in Celery
    fetch_and_store_channel_data.delay(channel_id)
    return jsonify({'status': 'Task submitted to fetch channel details'}), 202

@app.route('/playlistItems/<string:playlist_id>', methods=['GET'])
async def get_playlist_details(playlist_id):
    # Enqueue the task to fetch playlist details
    process_playlist.delay(playlist_id)
    return jsonify({'status': 'Task submitted to fetch playlist details'}), 202
