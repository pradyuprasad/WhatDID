from enum import Enum
from pydantic import BaseModel
from typing import Optional

class Browser(Enum):
    SAFARI = 'Safari'
    CHROME = 'Google Chrome'
    FIREFOX = 'Firefox'
    BRAVE = 'Brave Browser'
    EDGE = 'Microsoft Edge'

class WindowData(BaseModel):
    application_name: Optional[str]
    title: Optional[str]