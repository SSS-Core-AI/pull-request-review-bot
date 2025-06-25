from pydantic import BaseModel


class PullRequestInputModel(BaseModel):
    sha: str
    token: str

    patch_content: str
    comment_url: str
    fetch_file_url: str

class FileModel(BaseModel):
    sha: str
    filename: str
    status: str
    additions: int
    deletions: int
    changes: int
    blob_url: str
    raw_url: str
    contents_url: str
    patch: str
