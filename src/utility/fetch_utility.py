import httpx

async def fetch_github_file(content_url: str, file_path: str, sha: str, token: str) -> str:
    full_url = content_url.replace('{+path}', file_path)
    full_url += f'?ref={sha}'

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3.raw",
        "User-Agent": "Python-App/1.0"
    }
    try:
        with httpx.Client() as client:
            response = client.get(full_url, headers=headers)
            response.raise_for_status()
            return response.text
    except Exception as e :
        print(f'fetch_github_file: {full_url}', e)
        return ''