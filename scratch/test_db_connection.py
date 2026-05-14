import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
print(f"Testing connection to: {db_url.split('@')[-1]}") # Print only host for safety

try:
    engine = create_engine(db_url)
    with engine.connect() as connection:
        print("SUCCESS: Connection successful!")
except Exception as e:
    print("FAILED: Connection failed: " + str(e))
