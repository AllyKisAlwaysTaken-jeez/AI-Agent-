from pydantic import BaseModel

class AIRequest(BaseModel):
    section: str
    job_role: str
    keywords: str = ""
    project_info: str = ""

class LoginData(BaseModel):
    username: str
    password: str
