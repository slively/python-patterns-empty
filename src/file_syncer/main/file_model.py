from pydantic import BaseModel


class FileModel(BaseModel):
    name: str
    path: str
    is_dir: bool
    contents: str
