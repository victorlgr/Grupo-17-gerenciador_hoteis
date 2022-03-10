from waitress import serve
import logging
import app

logging.basicConfig(
    filename='error.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)
serve(app.app, host='127.0.0.1', port='80')
