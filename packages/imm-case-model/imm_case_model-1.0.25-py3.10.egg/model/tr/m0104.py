from typing import List
from model.common.trperson import Travel,Education
from model.common.commonmodel import CommonModel

class M0104Model(CommonModel):
    travel:List[Travel]
    education:List[Education]
    
    # initialize the model with a list of excels, which includes all nececcery information the model required. if outpuot_excel_file is not None, it will make an excel file.
    def __init__(self,excels=None,output_excel_file=None):
        if output_excel_file:
            import os
            path=os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
            excels=[
                path+'/template/excel/pa.xlsx'
            ]
        else:
            if excels is None and len(excels)==0:
                raise ValueError('You must input excel file list as source data for validation')
        super().__init__(excels,output_excel_file,globals())

