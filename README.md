# Face recognition + PostgreSQL (pgvector) example

Prereqs:
- PostgreSQL >= 13
- Create a database and set DATABASE_URL environment variable:
  export DATABASE_URL="postgres://user:pass@host:5432/dbname"
- In the DB run: CREATE EXTENSION IF NOT EXISTS pgvector;

Install Python deps:
  pip install -r requirements.txt

Create tables:
  python -c "from db import create_tables; create_tables()"

Enroll a person (from images):
  python enroll.py "Alice" alice1.jpg alice2.jpg

Recognize from an image:
  python recognize.py group_photo.jpg

Run webcam recognition:
  python recognize.py --webcam

Run the API:
  python app.py
