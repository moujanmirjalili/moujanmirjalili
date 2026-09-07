"""Refresh stats.json from the GitHub API, then rebuild the SVGs.

Environment:
  ACCESS_TOKEN  personal access token with 'repo' and 'read:user' scope
  USER_NAME     GitHub username (defaults to moujanmirjalili)

'views' sums the 14-day traffic view counts across all of your own repositories.
GitHub does not expose profile-page view counts through any API, so this is the
closest live figure available.
"""
import json, os, urllib.request, urllib.error

TOKEN = os.environ["ACCESS_TOKEN"]
USER = os.environ.get("USER_NAME", "moujanmirjalili")
HDRS = {"Authorization": f"bearer {TOKEN}", "User-Agent": USER,
        "Accept": "application/vnd.github+json"}

def rest(path):
    req = urllib.request.Request("https://api.github.com" + path, headers=HDRS)
    return json.load(urllib.request.urlopen(req))

def graphql(query, variables):
    body = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body,
                                 headers={**HDRS, "Content-Type": "application/json"})
    data = json.load(urllib.request.urlopen(req))
    if "errors" in data:
        raise SystemExit(data["errors"])
    return data["data"]

Q = """
query($login: String!, $cursor: String) {
  user(login: $login) {
    repositories(first: 100, after: $cursor, ownerAffiliations: OWNER) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes { name stargazerCount isFork }
    }
  }
}
"""

# --- stars, across every repo you own -------------------------------------
stars, names, cursor = 0, [], None
while True:
    repos = graphql(Q, {"login": USER, "cursor": cursor})["user"]["repositories"]
    for n in repos["nodes"]:
        stars += n["stargazerCount"]
        if not n["isFork"]:
            names.append(n["name"])
    if not repos["pageInfo"]["hasNextPage"]:
        break
    cursor = repos["pageInfo"]["endCursor"]

# --- views, summed from each repo's 14-day traffic ------------------------
views = 0
for name in names:
    try:
        views += rest(f"/repos/{USER}/{name}/traffic/views")["count"]
    except urllib.error.HTTPError as e:
        if e.code not in (403, 404):   # no traffic access on that repo
            raise

stats = {"stars": f"{stars:,}", "views": f"{views:,} (14 days)"}

here = os.path.dirname(os.path.abspath(__file__))
json.dump(stats, open(os.path.join(here, "stats.json"), "w"), indent=2)
print(json.dumps(stats, indent=2))
