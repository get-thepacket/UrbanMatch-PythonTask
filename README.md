# Marriage Matchmaking App

## Brief Description
The Marriage Matchmaking App is a simple backend application designed to help users find potential matches based on their profile information. The app allows users to create, read, update, and delete profiles with details such as name, age, gender, email, city, and interests.

## Prerequisites
- Python 3.7+
- FastAPI
- SQLAlchemy
- Postgres
- Alembic

## Steps to run
1. Install the requirements
   `pip install fastapi sqlalchemy alembic`
2. Add the database connection string in alembic.ini, at sqlalchemy.url
3. Run `alembic upgrade head`
3. Add the connection string using the .env.example and make a .env
4. Run the project by
   `fastapi dev main.py`
5. Use the provided postman collection to test.

## Assumptions
1. Match is based on same city with intersecting interests.
2. Genders are string based so couldn't do the opposite sex matching, currently every gender is matched.
3. Deletions are hard deletions