# FastAPI Address Book API

A minimal Address Book application built with FastAPI and SQLAlchemy.

## Features
- **CRUD Operations**: Create, Read, Update, and Delete addresses.
- **Coordinates**: Each address includes latitude and longitude.
- **Validation**: Ensures valid coordinate ranges.
- **Distance Search**: Find addresses within a specific distance (km) from a given location.
- **Local Persistence**: Uses SQLite for data storage.
- **Automatic Documentation**: Built-in Swagger UI.

## Prerequisites
- Python 3.8+ (Tested with 3.10)
- pip

## Installation

1. **Extract the project** to your preferred directory.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the FastAPI server:
```bash
python main.py
```
*Note: Depending on your system, you might need to use `py main.py` or `python3 main.py`.*

## Interactive API Documentation

Once the server is running, open your browser and navigate to:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Running Tests

To run the automated test suite:
```bash
pytest test_api.py
```
*Note: Use `py -m pytest test_api.py` if pytest is not in your PATH.*

## Project Structure
- `main.py`: Application entry point and API routes.
- `models.py`: SQLAlchemy database models.
- `schemas.py`: Pydantic data schemas and validation.
- `crud.py`: Database logic and distance calculation.
- `database.py`: Database connection and session setup.
- `test_api.py`: Automated test cases.
- `requirements.txt`: Project dependencies.
