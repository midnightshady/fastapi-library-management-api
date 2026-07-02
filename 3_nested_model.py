from pydantic import BaseModel

class Address(BaseModel):

    city : str
    state : str
    pin : int 

class Patient(BaseModel):
    
    name : str
    gender : str
    age : int
    address : Address

address_dict = {'city': 'Gurgaon', 'state': 'Haryana', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name':'Nitish', 'gender': 'Male', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)

# print(patient1)
# print(patient1.name)
# print(patient1.address.city)
# print(patient1.address.pin)

temp = patient1.model_dump(exclude={'address':['state']})

print(temp)