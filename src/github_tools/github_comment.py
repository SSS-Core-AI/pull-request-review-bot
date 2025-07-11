import httpx

async def send_github_comment(comment_url: str, comment_content: str, token: str,
                              sha: str = None, file_path: str = None, line_number: int = None):

    payload: dict[str, str | int] = {"body": comment_content}

    if sha is not None:
        payload["sha"] = sha

    if file_path is not None:
        payload["file_path"] = file_path

    if line_number is not None:
        payload["line_number"] = line_number

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(comment_url, json=payload, headers=headers)
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


