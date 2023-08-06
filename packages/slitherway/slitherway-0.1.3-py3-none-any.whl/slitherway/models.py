from typing import List, Optional

from pydantic import BaseModel


class FlywayCommandArgs(BaseModel):
    config_files: List[str] = []
    locations: List[str] = []
    user: Optional[str] = None
    password: Optional[str] = None
    url: Optional[str] = None
