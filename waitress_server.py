from waitress import serve
import logging
from app import app

logging.basicConfig(
    filename='error.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)
serve(app, host='0.0.0.0', port='80')
