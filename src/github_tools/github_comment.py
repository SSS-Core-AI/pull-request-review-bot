import os
import httpx

async def send_github_comment(comment_url: str, comment_content: str, token: str):

    payload = {"body": comment_content}
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


