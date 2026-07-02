from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Annotated, Literal
import json

app = FastAPI()
class Patient(BaseModel):
    id : Annotated[str, Field(..., description='Enter Patients ID', examples= ['P001', 'P002'])]

    name:Annotated[str, Field(...,max_length=10, description ='Enter Name Only 10 Chracters', examples = ['kaif', 'Nitish'])]

    age: Annotated[int, Field(...,gt = 0, lt = 100, description ='Enter Age Only Between 0 and 100')]

    gender : Annotated[Literal['male', 'female', 'others'], Field(..., description ='Enter Gender Of The Patient')]

    city: Annotated[str, Field(..., description ='Enter City Of The Patient')]

    height : Annotated[float, Field(..., description = 'Enter Height Of The Patient In Meters')]

    weight : Annotated[float, Field(..., description = 'Enter Weight Of The Patient In Kgs')]

    @computed_field
    @property
    def bmi(self) ->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) ->str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'
class PatientUpdate(BaseModel):
    name:Annotated[str, Field(..., description='Name Of The Patient', examples=['Kaif'])]
    city: Annotated[str, Field(..., description='Enter City Of The Patient')]
    age: Annotated[int, Field(...,gt = 0, lt = 100, description='Enter Age Of The Patient In Years')]
    gender: Annotated[Literal['male', 'female', 'other'],Field(..., description='Enter Gender Of The Patient')]
    height: Annotated[float, Field(..., description='Enter Height Of The Patient In Mtrs')]
    weight:Annotated[float, Field(..., description='Enter Weight Of The Patient In Kgs')]

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get('/')
def hello():
    return{'message':'Hello World'}

@app.get("/xyz")
def xyz():
    return {"api": "patient"}

@app.get('/about')
def about():
    return{'message':'A Fully Function API To Manage Patient Recors'}

@app.get('/view')
def patient_list():
    data = load_data()
    return data

@app.get('/patients/{patient_id}')
def view_patient(patient_id: str = Path(..., description='Enter Patients ID', examples=['P001', 'P002', 'P003'])):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code= 404, detail='Patient Not Found')
    else:
        return data[patient_id]
    
@app.get('/sort')
def sort(sort:str = Query(..., description='Sort Will Be On The Base On Height, Weight Or BMI', ), order:str= Query('asc', description='Sort In The Base Of asc or dsc')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort not in valid_fields:
        raise HTTPException(status_code = 400, detail=f'Enter Valid Field Froms {valid_fields}')
    
    if order not in ['asc', 'dsc']:
        raise HTTPException(status_code=400, detail='Enter Sort Order Only In ASC Or DSC Order')
    data = load_data()

    sort_order = True if order == 'dsc' else False  

    sorted_data = sorted(data.values(), key = lambda x:x.get(sort, 0), reverse = sort_order)
    return sorted_data 

@app.post('/create')
def patient_id(patient:Patient):

    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code= 400, detail='Patient Already Exists')
    
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'Patieent Created Successfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id:str, patient_update: PatientUpdate):

    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient Not Found')   
    exisiting_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        exisiting_patient_info[key] = value

    pydantic_patient_obj = Patient(**exisiting_patient_info)

    exisiting_patient_info = pydantic_patient_obj.model_dump(exclude='id')

    data[patient_id] = exisiting_patient_info

    save_data(data)

    return JSONResponse(status_code=200, content= {'message':'Patient Id Updated Successfully'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail = 'Patient Not Found')

    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200, content= {'message':'Patient Deleted'})


# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def home():
#     return {"message": "Patient API"}

# @app.get("/xyz")
# def xyz():
#     return {"api": "patient"}