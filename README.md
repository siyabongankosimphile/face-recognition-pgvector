# Docker & production instructions added

## Docker

Build and run with docker-compose (this will start Postgres + the web app):

  docker-compose up --build

The web app will be available at http://localhost:5000 and the database at port 5432.

The docker-compose file creates a `postgres` DB user with password `example`. Change these values in `docker-compose.yml` for production.

## Production notes

- The app runs under Gunicorn in the Docker image.
- SECRET_KEY, DATABASE_URL and other sensitive settings should be provided via environment variables or a secrets manager in production — do not use the default `change-me-in-production` secret.
- For large-scale or high-throughput deployments consider replacing `face_recognition` (dlib) with a GPU-backed model and using a model server for inference.

## Web dashboard

A minimal web dashboard is available at `/` for enrolling and recognizing faces via file uploads.

