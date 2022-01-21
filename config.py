import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('CLEARDB_DATABASE_URL')
