import os
from dotenv import load_dotenv
load_dotenv()

config = {
    'OPENAI_API_KEY': os.environ['OPENAI_API_KEY'],
    'OPENAI_API_ENDPOINT': os.environ['OPENAI_API_ENDPOINT'],
    'OPENAI_API_MODEL': os.environ['OPENAI_API_MODEL'],
    'STATIC_CONTENT_ENDPOINT': os.environ.get('STATIC_CONTENT_ENDPOINT', 'http://127.0.0.1:8000')
}
