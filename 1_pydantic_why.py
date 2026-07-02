from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated 

class Patient(BaseModel):

    name:str = Annotated[str, Field(max_length=50, title= "Name Of The Patient", description = "Give The Name Of The Patient In less Than 50", examples=['Nitish', 'Kaif', 'Amit'])]
    email:EmailStr
    age:int = Field(gt = 18, lt = 100)
    allergies:Annotated[Optional[List[str]], Field(default = None,max_length= 5)]
    contact: Dict[str, str]
    married: Annotated[Optional[bool], Field(default=None, description='Is The Patient Married?')]
    linked_in: AnyUrl
    weight:Annotated[float, Field(gt = 0, strict = True)]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):

        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError("Not A Valid Domain")
        
        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.capitalize().strip()
    
    @field_validator("allergies")
    @classmethod
    def allergie_spit(cls, value):
        return value.join(['pollen', 'dust'])

def updated_value(patient:Patient): 

    print("Name: ",patient.name)
    print('Age: ', patient.age)
    print("married:", patient.married)
    print("Allergies: ", patient.allergies)
    print('Contact: ', patient.contact)
    print("Email: ", patient.email)
    print("Linkedin: ", patient.linked_in)
    print("Weight:" , patient.weight)
    print('updated')

pateint_info = {'name':'kaif', 'age': 19,'email':"abc@hdfc.com", 'allergies':['pollen', 'dust'], 'contact':{'phone':'123456789', 'email':'kaifqureshi36720'}, 'linked_in':"http://linkedin.com/1322", 'weight': 75.1 }

patient1 = Patient(**pateint_info)
updated_value(patient1)