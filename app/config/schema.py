from datetime import datetime
from typing import Optional
from pydantic import BaseModel
class passNum(BaseModel):
    pass0:Optional[str] = None
    pass1:Optional[str] = None
    pass2:Optional[str] = None
    pass3:Optional[str] = None
    pass4:Optional[str] = None
    pass5:Optional[str] = None
class crePass(BaseModel):
    pass0: str
    pass1: str
    pass2: str
    pass3: str
    pass4: str
    pass5: str

class think_(BaseModel):
    think_id: Optional[int] = None
    title: str
    contents: str
    think_class: int
    think_source: Optional[int] = None
    think_filePath: Optional[str] = None
    think_fileName: Optional[str] = None
    think_creDate: Optional[datetime] = None
    think_editDate: Optional[datetime] = None

class search_(BaseModel):
    search_tag_0: Optional[int] = None
    search_tag_1: Optional[int] = None
    search_tag_2: Optional[int] = None
    search_tag_3: Optional[int] = None
    search_tag_4: Optional[int] = None
    search_subclass: Optional[int] = None
    search_source: Optional[int] = None
