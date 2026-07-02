from fastapi import FastAPI, Path, Query, HTTPException
import json
from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Optional
from fastapi.responses import JSONResponse

app = FastAPI()

class Book(BaseModel):
    id:Annotated[str, Field(...,description='Enter The Id Of The Book', examples=['B001'])]

    title:Annotated[str, Field(..., description='Enter Title of The Book', examples=["The Great Gatsby"])]

    author:Annotated[str, Field(..., description='Enter Author Of The Book', examples=['Suzanne Collins'])]

    genre:Annotated[str, Field(..., description='Enter Genre Of The Book', examples=['Fiction'])]

    published_year:Annotated[int, Field(..., description='Enter Year Of Publish Only In Integer', examples=['2008'])]

    price:Annotated[int, Field(..., description='Enter Price Of The Book', examples=['799'])]

    available:Annotated[bool, Field(default = False, description='Enter If The Book Is Available')]

    @field_validator('title', 'author', 'genre')
    @classmethod
    def capital_title(cls, value):
        return value.strip().title()
    
class BookUpdate(BaseModel):

    title : Annotated[Optional[str], Field(default=None)]
    id :  Annotated[Optional[str], Field(default=None)]
    author: Annotated[Optional[str], Field(default=None)]
    genre: Annotated[Optional[str], Field(default=None)]
    published_year: Annotated[Optional[int], Field(default=None)]
    price: Annotated[Optional[int], Field(default=None)]
    available:Annotated[Optional[bool], Field(default=None)]


    @field_validator('title', 'author', 'genre')
    @classmethod
    def capital_title(cls, value):
        return value.strip().title()

def load_data():
    with open('library_data.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('library_data.json', 'w') as f:
        json.dump(data, f)

@app.get('/')
def home():
    return{'message':'Welcome Home'}

@app.get('/about')
def about():
    return{'message':'A Fully Functional API To Manage Library Records'}

@app.get('/books')
def records():
    data = load_data()
    return data

@app.get('/books/{book_id}')
def view_book(book_id:str = Path(..., description='Enter The Id Of The Required Book: ', example='B001')):

    data = load_data()
    if book_id not in data:
        raise HTTPException(status_code= 404, detail='Book With This Id Not Found')
    
    return data[book_id]

@app.post('/enter')
def new_book(book: Book):
    data = load_data()

    if book.id in data:
        raise HTTPException(status_code=400, detail='Book Already Exist')
    
    data[book.id] = book.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201, content={'message':'ID Created Successfully'})

@app.put('/books/{book_id}')
def update_book(book_id : str, book_update:BookUpdate):
    data = load_data()

    if book_id not in data:
        raise HTTPException(status_code=404, detail='Book With This ID Is Not Avaiable')
    
    existing_book_info = data[book_id]
    updated_book_info = book_update.model_dump(exclude_unset=True)

    for key,value in updated_book_info.items():
        existing_book_info[key] = value

    existing_book_info['id'] = book_id
    existing_book_pydantic_obj = Book(**existing_book_info)
    existing_book_info = existing_book_pydantic_obj.model_dump(exclude = 'id')

    data[book_id] = existing_book_info
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'Book Updated Successfully'})

@app.delete('/book/{book_id}')
def remove_book(book_id:str):
    data = load_data()

    if book_id not in data:
        raise HTTPException(status_code=404, detail="Book With This ID Not Found")
    del data[book_id]
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'Book With This Id Deleted'})