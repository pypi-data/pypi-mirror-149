from datetime import date
from pydantic import BaseModel,EmailStr
from typing import List,Union

class COR(BaseModel):
    start_date:date
    end_date:Union[date,None]
    country:str
    status:str
    


class CORs(object):
    def __init__(self, cors: List[COR]):
        self.cors=cors
    
    @property
    def current(self):
        ccor=[ country for country in self.cors if country.end_date==None]
        if len(ccor)==1:
            return ccor[0]
        elif len(ccor)==0:
            raise ValueError('There is required that the first line of current/past country of residence must leave the end date blank to show it is current residence ')
        else:
            raise ValueError('There are more than one end date blank, which means you are living in different countries at same time currently. ')
