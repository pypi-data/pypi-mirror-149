from functools import reduce
from pydantic import BaseModel,validator
from datetime import date
from typing import Optional,List
from model.common.mixins import DurationMixin
from model.common.utils import makeList,normalize

"""
with properties of start_from and end_to got from mixin
"""
class EducationBase(BaseModel,DurationMixin):
    start_date: date
    end_date:Optional[date]
    school_name: str
    education_level:str
    field_of_study:str
    
    _normalize_school_name=validator('school_name',allow_reuse=True,check_fields=False)(normalize)
    _normalize_field_of_study=validator('field_of_study',allow_reuse=True,check_fields=False)(normalize)
    
    @validator("end_date")
    def endDateBigger(cls,end_date,values):
        start_date=values.get('start_date')
        the_date=end_date if end_date else date.today()
        if (the_date-start_date).days<=0:
            raise ValueError(f'End date {the_date} is earlier than start date {start_date}')
        end_date=end_date if end_date else "Present"
        return end_date

class EducationHistory():
    def __init__(self,edu_list:List[EducationBase]):
        self.edu_list=edu_list
    
    # total education years
    @property
    def years(self):
        return reduce(lambda a,b:a.lengthOfYears+b.lengthOfYears,self.edu_list)
    
    @property
    def highest(self):
        education_level={
            "None": 0,
            "High school": 1,
            "Certificate/Diploma(Trade)": 2,
            "Diploma/Certificate": 3,
            "Associate": 4,
            "Bachelor": 5,
            "Post-graduate diploma": 6,
            "Master": 7,
            "Doctor": 8
        }
        highest_num=max([ education_level[edu.education_level] for edu in self.edu_list])
        for k,v in education_level.items():
            if v==highest_num:
                return k

    @property
    def highestEducation(self):
        highest_edu=[edu for edu in self.edu_list if edu.education_level==self.highest]
        if len(highest_edu)>0: return highest_edu[0]