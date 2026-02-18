import unittest
from unittest.mock import patch, MagicMock

import github_api
from github_api import (
    get_user_repos,
    get_repo_commit_count,
    get_user_repo_commit_counts,
    GitHubAPIError,
)


class TestGitHubAPI(unittest.TestCase):

    @patch("github_api.requests.get")
    def test_get_user_repos_happy_path(self, mock_get):
        # Fake /users/<username>/repos response
        fake_repos = [
            {"name": "Triangle567"},
            {"name": "Square567"},
        ]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = fake_repos
        mock_get.return_value = mock_response

        repos = get_user_repos("John567")

        self.assertEqual(repos, ["Triangle567", "Square567"])
        mock_get.assert_called_once_with(
            "https://api.github.com/users/John567/repos"
        )

    @patch("github_api.requests.get")
    def test_get_user_repos_non_200_status(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Not Found"}
        mock_get.return_value = mock_response

        with self.assertRaises(GitHubAPIError):
            get_user_repos("unknown_user")

    @patch("github_api.requests.get")
    def test_get_user_repos_unexpected_json_format(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"not": "a list"}
        mock_get.return_value = mock_response

        with self.assertRaises(GitHubAPIError):
            get_user_repos("John567")

    def test_get_user_repos_invalid_username(self):
        with self.assertRaises(ValueError):
            get_user_repos("")
        with self.assertRaises(ValueError):
            get_user_repos(None)

    @patch("github_api.requests.get")
    def test_get_repo_commit_count_happy_path(self, mock_get):
        # Fake /repos/<username>/<repo>/commits response
        fake_commits = [{}, {}, {}]  # length 3

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = fake_commits
        mock_get.return_value = mock_response

        count = get_repo_commit_count("John567", "Triangle567")

        self.assertEqual(count, 3)
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/John567/Triangle567/commits"
        )

    @patch("github_api.requests.get")
    def test_get_repo_commit_count_non_200_status(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Server error"}
        mock_get.return_value = mock_response

        with self.assertRaises(GitHubAPIError):
            get_repo_commit_count("John567", "Triangle567")

    @patch("github_api.requests.get")
    def test_get_repo_commit_count_unexpected_json_format(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"not": "a list"}
        mock_get.return_value = mock_response

        with self.assertRaises(GitHubAPIError):
            get_repo_commit_count("John567", "Triangle567")

    def test_get_repo_commit_count_invalid_args(self):
        with self.assertRaises(ValueError):
            get_repo_commit_count("", "repo")
        with self.assertRaises(ValueError):
            get_repo_commit_count("user", "")
        with self.assertRaises(ValueError):
            get_repo_commit_count(None, "repo")

    @patch("github_api.get_repo_commit_count")
    @patch("github_api.get_user_repos")
    def test_get_user_repo_commit_counts_combined(
        self, mock_get_user_repos, mock_get_repo_commit_count
    ):
        mock_get_user_repos.return_value = ["Triangle567", "Square567"]

        # First repo returns 10 commits, second raises GitHubAPIError
        def side_effect(username, repo_name):
            if repo_name == "Triangle567":
                return 10
            else:
                raise GitHubAPIError("API error")

        mock_get_repo_commit_count.side_effect = side_effect

        result = get_user_repo_commit_counts("John567")

        self.assertEqual(
            result,
            [("Triangle567", 10), ("Square567", 0)],
        )

    @patch("github_api.get_repo_commit_count")
    @patch("github_api.get_user_repos")
    def test_get_user_repo_commit_counts_empty_repos(
        self, mock_get_user_repos, mock_get_repo_commit_count
    ):
        mock_get_user_repos.return_value = []

        result = get_user_repo_commit_counts("John567")
        self.assertEqual(result, [])
        mock_get_repo_commit_count.assert_not_called()


if __name__ == "__main__":
    unittest.main()
