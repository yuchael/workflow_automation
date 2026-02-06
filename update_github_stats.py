# update_github_stats.py
# pip install requests python-dotenv

import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GIT_TOKEN = os.getenv("GIT_TOKEN")
USERNAME = "YOUR_GITHUB_ID"  # 👉 본인 GitHub 아이디로 수정

HEADERS = {
    "Authorization": f"token {GIT_TOKEN}"
}

README_PATH = "README.md"

def get_github_stats():
    url = f"https://api.github.com/users/{USERNAME}"
    repos_url = f"https://api.github.com/users/{USERNAME}/repos"

    user_res = requests.get(url, headers=HEADERS)
    repos_res = requests.get(repos_url, headers=HEADERS)

    if user_res.status_code == 200 and repos_res.status_code == 200:
        user_data = user_res.json()
        repos_data = repos_res.json()

        repo_count = user_data["public_repos"]
        followers = user_data["followers"]
        following = user_data["following"]

        total_stars = sum(repo["stargazers_count"] for repo in repos_data)

        return {
            "repo_count": repo_count,
            "followers": followers,
            "following": following,
            "stars": total_stars
        }
    else:
        return None


def update_readme():
    stats = get_github_stats()
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    if stats:
        content = f"""
# GitHub Stats Auto Update 🤖

이 리포지토리는 GitHub API를 활용해 내 GitHub 활동 정보를 자동 업데이트합니다.

## 📊 현재 GitHub 상태
- 📦 Public Repos: {stats['repo_count']}
- ⭐ Total Stars: {stats['stars']}
- 👥 Followers: {stats['followers']}
- 🔗 Following: {stats['following']}

⏳ 업데이트 시간: {now} (UTC)

---
자동 업데이트 봇에 의해 관리됩니다.
"""
    else:
        content = "GitHub 정보를 가져오는 데 실패했습니다."

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    update_readme()
