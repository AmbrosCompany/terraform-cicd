"""Utilities for Cathcart-Dispatch."""

import os
from typing import Union

import requests


def create_issue_comment(
    github_repo: str,
    issue_number: str,
    comment_body: str,
    github_token: str,
) -> requests.Response:
    """Commenting on GH Issue."""
    url = f"https://api.github.com/repos/{github_repo}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # colored_comment_body = "```diff\n- " + comment_body + "\n```"
    colored_comment_body = "```yaml\n" + comment_body + "\n```"
    data = {"body": colored_comment_body}
    response = requests.post(url, headers=headers, json=data)
    return response


def set_output(name: str, value: str) -> None:
    """Set output to GH Env."""
    with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
        print(f"{name}={value}", file=fh)


def check_if_pr_approved(
    github_repo: str,
    issue_number: str,
    github_token: str,
) -> Union[None, str]:
    """Confirm whether PR is approved."""
    url = f"https://api.github.com/repos/{github_repo}/pulls/{issue_number}/reviews"

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        reviews = response.json()
        # Check if there are any reviews with "APPROVED" state
        if any(review["state"] == "APPROVED" for review in reviews):
            print("Pull request has been approved!")
            return "approved"
            # Perform actions for approved pull requests here
        else:
            print("Pull request has not been approved yet.")
            # Perform actions for pull requests without approval here
    else:
        print(f"Failed to get reviews. Status code: {response.status_code}")
