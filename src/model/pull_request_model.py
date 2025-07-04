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


class PullRequestIssueModel(BaseModel):
    issue_title: str = Field(default='', description='The title of the issue')
    priority: str = Field(default='low', description='how serious is the issue, categorize into high, middle and low')
    content: str = Field(default='', description='Follow the [Instruction]')