import httpx

async def send_github_comment(comment_url: str, comment_content: str, token: str,
                              sha: str = None, file_path: str = None, line_number: int = None):

    payload: dict[str, str | int] = {"body": comment_content}

    if line_number is not None and file_path is not None and sha is not None:
        payload["line"] = line_number
        payload["path"] = file_path
        payload["commit_id"] = sha
        payload["side"] = 'RIGHT'

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(comment_url, json=payload, headers=headers)

        print('send_github_comment response', response.text)
        return response

async def fetch_github_content(url: str, token: str):

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()


