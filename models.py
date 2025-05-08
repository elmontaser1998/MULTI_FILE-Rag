from pydantic import BaseModel, Field, field_validator
from typing import Annotated


class ChatTurn(BaseModel):
    question: str
    answer: str
    
class UserQuestion(BaseModel):
    text: Annotated[str, Field(min_length=5, max_length=200)]
    
    
class UploadedFileInfo(BaseModel):
    filename: str

    @field_validator("filename")
    def check_extension(cls, v):
        if not v.endswith((".pdf", ".docx", ".csv")):
            raise ValueError("Invalid file type")
        return v