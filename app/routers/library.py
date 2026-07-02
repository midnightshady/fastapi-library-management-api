from fastapi import APIRouter, Query, Path, HTTPException
from fastapi.responses import JSONResponse

from app.schemas import Book, BookUpdate
from app.database import load_data, save_data

router = APIRouter()

@router.get('/')
def home():
    return{'message':'Welcome Home'}

@router.get('/about')
def about():
    return{'message':'A Fully Functional API To Manage Library Records'}

@router.get('/books')
def records():
    data = load_data()
    return data

@router.get('/books/{book_id}')
def view_book(book_id:str = Path(..., description='Enter The Id Of The Required Book: ', example='B001')):

    data = load_data()
    if book_id not in data:
        raise HTTPException(status_code= 404, detail='Book With This Id Not Found')
    
    return data[book_id]

@router.post('/enter')
def new_book(book: Book):
    data = load_data()

    if book.id in data:
        raise HTTPException(status_code=400, detail='Book Already Exist')
    
    data[book.id] = book.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201, content={'message':'ID Created Successfully'})

@router.put('/books/{book_id}')
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

@router.delete('/book/{book_id}')
def remove_book(book_id:str):
    data = load_data()

    if book_id not in data:
        raise HTTPException(status_code=404, detail="Book With This ID Not Found")
    del data[book_id]
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'Book With This Id Deleted'})