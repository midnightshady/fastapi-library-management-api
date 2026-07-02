from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Optional
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