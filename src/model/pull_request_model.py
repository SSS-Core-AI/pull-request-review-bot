from pydantic import BaseModel


class PullRequestInputModel(BaseModel):
    sha: str
    token: str

    patch_content: str
    comment_url: str
    fetch_file_url: str