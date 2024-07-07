from datetime import datetime
from typing import Optional
from pydantic import BaseModel
class passNum(BaseModel):
    pass0:Optional[int|str] = None
    pass1:Optional[int|str] = None
    pass2:Optional[int|str] = None
    pass3:Optional[int|str] = None
    pass4:Optional[int|str] = None
    pass5:Optional[int|str] = None

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