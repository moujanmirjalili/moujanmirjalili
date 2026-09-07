"""Refresh stats.json from the GitHub API, then rebuild the SVGs.

Run locally or from the bundled GitHub Action. Needs two environment variables:
  ACCESS_TOKEN  a personal access token with 'repo' and 'read:user' scope
  USER_NAME     your GitHub username
"""
import json, os, urllib.request, datetime

TOKEN = os.environ["ACCESS_TOKEN"]
USER = os.environ.get("USER_NAME", "moujanmirjalili")
GQL = "https://api.github.com/graphql"

def query(q, variables):
    body = json.dumps({"query": q, "variables": variables}).encode()
    req = urllib.request.Request(GQL, data=body, headers={
        "Authorization": f"bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": USER,
    })
    data = json.load(urllib.request.urlopen(req))
    if "errors" in data:
        raise SystemExit(data["errors"])
    return data["data"]

Q = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    following { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
      totalCount
      nodes { stargazerCount }
    }
    contributionsCollection { totalCommitContributions restrictedContributionsCount }
  }
}
"""

u = query(Q, {"login": USER})["user"]
created = datetime.datetime.fromisoformat(u["createdAt"].replace("Z", "+00:00"))
stars = sum(n["stargazerCount"] for n in u["repositories"]["nodes"])
commits = (u["contributionsCollection"]["totalCommitContributions"]
           + u["contributionsCollection"]["restrictedContributionsCount"])

stats = {
    "repos": str(u["repositories"]["totalCount"]),
    "followers": str(u["followers"]["totalCount"]),
    "following": str(u["following"]["totalCount"]),
    "member_since": created.strftime("%B %Y"),
    "stars": str(stars),
    "commits": f"{commits:,} (past year)",
}

here = os.path.dirname(os.path.abspath(__file__))
json.dump(stats, open(os.path.join(here, "stats.json"), "w"), indent=2)
print(json.dumps(stats, indent=2))
