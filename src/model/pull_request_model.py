from typing import Optional

from pydantic import BaseModel, Field


class PullRequestInputModel(BaseModel):
    sha: str
    token: str

    patch_content: str
    comment_url: str
    fetch_file_url: str

class FileModel(BaseModel):
    filename: str
    status: str
    raw_content: Optional[str] = Field(default='')