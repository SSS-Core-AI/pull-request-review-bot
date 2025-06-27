from __future__ import annotations
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
    raw_content: Optional[str] = Field(default='')
    dependency_paths: Optional[list[str]] = Field(default=[])