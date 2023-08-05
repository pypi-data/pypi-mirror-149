from pydantic import BaseModel
from termcolor import colored
from functools import reduce
from typing import List,Optional
from model.common.address import Address
from model.common.phone import Phone
from model.common.commonmodel import CommonModel
from datetime import date

class Family(BaseModel):
    last_name:str
    first_name:str	
    native_last_name:Optional[str]	
    native_first_name:Optional[str] 
    date_of_birth:date  
    date_of_death:Optional[date]
    place_of_birth:str
    birth_country:str 
    relationship:str
    
class Personal(BaseModel):
    last_name:str
    first_name:str
    native_last_name:str
    native_first_name:str
    date_of_birth:date	

class PRBackground(BaseModel):
    q1:bool
    q2:bool
    q3:bool
    q4:bool
    q5:bool
    q6:bool
    q7:bool
    q8:bool
    q9:bool
    q10:bool
    q11:bool
    details:Optional[str]

class Education(BaseModel):
    start_date:Optional[date]
    end_date:Optional[date]
    school_name:Optional[str]
    city:Optional[str]
    country:Optional[str]
    education_level:Optional[str]	
    field_of_study:Optional[str]

class History(BaseModel):
    start_date:date
    end_date:date	
    activity:str	
    city_and_country:str	
    status:str	
    name_of_company_or_school:str

class Member(BaseModel):
    start_date:date	
    end_date:date	
    organization_name:str	
    organization_type:str	
    position:str	
    city:str	
    country:str

class Government(BaseModel):
    start_date:date	
    end_date:date	
    country:str	
    department:str	
    position:str

class Military(BaseModel):
    start_date:date	
    end_date:date	
    location:str	
    province:str	
    country:str	
    service_detail:str	
    rank:str	
    combat_detail:Optional[str]	
    reason_for_end:Optional[str]

class AddressHistory(BaseModel):
    start_date:date	
    end_date:date	
    street_and_number:str	
    city:str	
    province:str	
    country:str	
    post_code:str    
        
class M5669Model(CommonModel):
    personal:Personal
    family:List[Family]
    prbackground:PRBackground
    education:List[Education]
    history:List[History]
    member:List[Member]
    government:List[Government]
    military:List[Military]
    addresshistory:List[AddressHistory]

    
    # initialize the model with a list of excels, which includes all nececcery information the model required. if outpuot_excel_file is not None, it will make an excel file.
    def __init__(self,excels=None,output_excel_file=None):
        if output_excel_file:
            import os
            path=os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
            excels=[
                path+'/template/excel/pr.xlsx',
                path+'/template/excel/pa.xlsx'
            ]
        else:
            if excels is None and len(excels)==0:
                raise ValueError('You must input excel file list as source data for validation')
        super().__init__(excels,output_excel_file,globals())