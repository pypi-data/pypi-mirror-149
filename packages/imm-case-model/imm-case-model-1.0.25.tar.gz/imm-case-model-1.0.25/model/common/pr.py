from datetime import date
from pydantic import BaseModel
from typing import Optional
from model.common.person import Person

class PrCase(BaseModel):
    applying_country:str
    applying_stauts:str
    applying_start_date:date
    applying_end_date:date
    
# PR education is different from TR
class Education(BaseModel):
    highest_level:str
    years_of_education:int
    current_occupation:str
    intended_occupation:str
        
# Pr Personal has a little more properties than general person's 
class PrPersonal(Person):
    height:int
    eye_color:str
    


    
    


    
