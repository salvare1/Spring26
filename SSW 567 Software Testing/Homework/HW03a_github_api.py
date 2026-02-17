import requests


class GitHubAPIError(Exception):
    """Custom exception for GitHub API related errors."""
    pass


def get_user_repos(username):
    """
    Return a list of repository names for the given GitHub username.
    """
    if not username or not isinstance(username, str):
        raise ValueError("username must be a non-empty string")

    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code != 200:
        raise GitHubAPIError(
            f"Failed to fetch repos for user '{username}'. "
            f"Status code: {response.status_code}"
        )

    repos_json = response.json()
    # Handle case where GitHub might return something unexpected
    if not isinstance(repos_json, list):
        raise GitHubAPIError("Unexpected response format for repos")

    repo_names = [repo.get("name") for repo in repos_json if "name" in repo]
    return repo_names


def get_repo_commit_count(username, repo_name):
    """
    Return the number of commits for a given user/repo.
    Uses length of returned JSON array from commits endpoint.
    WARNING: This does NOT handle pagination; for this assignment,
    we assume the simple case that all commits are on the first page.
    """
    if not username or not isinstance(username, str):
        raise ValueError("username must be a non-empty string")
    if not repo_name or not isinstance(repo_name, str):
        raise ValueError("repo_name must be a non-empty string")

    url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    response = requests.get(url)

    if response.status_code != 200:
        raise GitHubAPIError(
            f"Failed to fetch commits for '{username}/{repo_name}'. "
            f"Status code: {response.status_code}"
        )

    commits_json = response.json()
    if not isinstance(commits_json, list):
        raise GitHubAPIError("Unexpected response format for commits")

    return len(commits_json)


def get_user_repo_commit_counts(username):
    """
    Given a GitHub username, return a list of (repo_name, commit_count) tuples.
    Example:
      [("Triangle567", 10), ("Square567", 27)]
    """
    repo_names = get_user_repos(username)
    results = []

    for repo_name in repo_names:
        try:
            commit_count = get_repo_commit_count(username, repo_name)
        except GitHubAPIError:
            # From a tester perspective, we don't want one bad repo
            # to kill the whole result set. We could log or mark as 0.
            commit_count = 0
        results.append((repo_name, commit_count))

    return results


def print_user_repo_commit_counts(username):
    """
    Convenience function that prints in the required format.
    This is a thin wrapper so core logic is testable separately.
    """
    repo_commit_counts = get_user_repo_commit_counts(username)
    for repo_name, count in repo_commit_counts:
        print(f"Repo: {repo_name} Number of commits: {count}")
