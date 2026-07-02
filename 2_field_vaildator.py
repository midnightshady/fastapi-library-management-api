from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field 
from typing import Dict, List, Annotated

class Patient(BaseModel):
    name:Annotated[str, Field(max_length= 50, description='Enter The Name Under 50 Characters', title='Enter The Name', examples=['Nitish', 'Kaif'])]
    email: EmailStr
    linkedin: AnyUrl
    age:int
    allergies:Annotated[List[str], Field(default = None, max_length = 5, strict = True)]
    contact:Dict[str, str]
    weight:Annotated[float, Field(ls = 100, gt = 0, detail= 'Enter Weight Of The Patient', strict=True)]
    city: str
    married: Annotated[bool, Field(default=False, description='Is The Patient Married Or Not')]
    height: Annotated[float, Field(description='Enter Patients height')]

    @field_validator('email')
    @classmethod
    def email_validaotor(cls, value):
        valid_domains = ['hdfc.com', 'icici.com'] 
        domain_name = value.split('@')[-1]
 
        if domain_name not in valid_domains:
            raise ValueError('Not a Valid Domain')
        return value
    
    @field_validator('name')
    @classmethod
    def update_name(cls, value):
        return value.capitalize().strip()
    
    @field_validator('age')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            ValueError("Age Shold Be Between Under 0 and 100")

    @model_validator(mode = 'after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact:
            raise ValueError('Emergency Number Not In Contact Details')
        else:
            return model
        
    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi

def update_patient(patient: Patient):
    print('Name: ', patient.name)
    print('Age: ', patient.age)
    print('Allergies: ', patient.allergies)
    print('Contact: ', patient.contact)
    print('Weight: ', patient.weight)
    print('City: ', patient.city)
    print('Email: ', patient.email)
    print('Linkedin: ', patient.linkedin)
    print('Married: ', patient.married)
    print('BMI: ', patient.calculate_bmi)

patient_info = {'name': 'kaif', 'age': '65', 'allergies':['Dust', 'Pollen',], 'weight': 2.1, 'city': 'Mumbai', 'contact':{'phone':'8698701372', 'emergency':'123456789'}, 'email': 'abc@hdfc.com', 'linkedin':'httpps://linkedin.com', 'height': 1.72}

patient1 = Patient(**patient_info)
update_patient(patient1)