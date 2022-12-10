# Simple Python interface for OpenAI API
A python interface for interacting with the openai api. This allows a user class to claim ownership of images created
## Requirements
- Python3 >=3.9


## Features
- SQLAlchemy
- Pydantic

## File Structure
```
.
├── api
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
|   ├── models.py
|   ├── schemas.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── helpers
│       ├── __init__.py
│       └── crud.py
```

## Quick Start
1. Clone the repo:
    ```bash
    git clone https://github.com/WMRamadan/fastapi-boilerplate
    cd fastapi-boilerplate
    ```
2. Initialize and activate a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```
4. Create any env variables.  
    a. `touch .env`  
    b. Add line `SECRET_KEY='<YOUR OPEN AI API KEY>'`
    
4. Run the development server:
    ```bash
    uvicorn api.main:app --reload
    ```

5. View the API docs:
    ```bash
    http://localhost:8000/docs
    # OR
    http://localhost:8000/redoc
    ```
