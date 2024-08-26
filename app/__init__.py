from quart import Quart
from celery import Celery
from app.config import Config
from app.database import create_db_pool

app = Quart(__name__)

# Initialize Celery
def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    return celery

# Load configuration
app.config.from_object(Config)
celery = make_celery(app)

@app.before_serving
async def init_db_pool():
    await create_db_pool()

@app.after_serving
async def close_db_pool():
    await db_pool.close()
