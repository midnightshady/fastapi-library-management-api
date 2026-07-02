# 📚 FastAPI Library Management API

A RESTful CRUD API built using **FastAPI** and **Pydantic** to manage library records.

## 🚀 Features

- Create a new book
- View all books
- View a book by ID
- Update book details
- Delete a book
- Input validation using Pydantic
- JSON file as database

## 🛠️ Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn
- JSON

## 📂 Project Structure

```
fastapi-library-management-api
│
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── database.py
│   └── routers
│       ├── __init__.py
│       └── library.py
│
├── data
│   └── library_data.json
│
├── requirements.txt
├── README.md
└── .gitignore
```

## 📌 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Home |
| GET | /about | About API |
| GET | /books | Get all books |
| GET | /books/{book_id} | Get book by ID |
| POST | /enter | Add a new book |
| PUT | /books/{book_id} | Update a book |
| DELETE | /book/{book_id} | Delete a book |

## ▶️ Run Locally

Clone the repository

```bash
git clone <repository-url>
```

Go to the project directory

```bash
cd fastapi-library-management-api
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the server

```bash
uvicorn app.main:app --reload
```

Open Swagger UI

```
http://127.0.0.1:8000/docs
```

## 👨‍💻 Author

Kaif Qureshi