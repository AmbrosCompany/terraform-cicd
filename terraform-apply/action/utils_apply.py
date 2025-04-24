"""Utilities for Terraform workflows."""

import os
from typing import Union

import requests


def create_issue_comment(
    github_repo: str,
    issue_number: str,
    comment_body: str,
    github_token: str,
) -> Union[requests.Response, None]:
    """Create a comment on a specific GitHub issue."""
    if not comment_body:
        return
    url = f"https://api.github.com/repos/{github_repo}/issues/{issue_number}/comments"
    print(url)
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    if "Saved plan is stale" in comment_body:
        comment_body = (
            "Saved plan is stale."
            " The given plan file can no longer be applied because"
            " the state was changed by another operation"
            " after the plan was created"
        )
    elif "Apply complete!" in comment_body:
        extract_valid_message = comment_body.split("Apply complete!")[1]
        comment_body = "Apply complete! " + extract_valid_message.split(".")[0]

    else:
        extract_valid_message = comment_body.split("no-color")
        comment_body = extract_valid_message[1]

    colored_comment_body = "```diff\n- " + comment_body + "\n```"
    data = {"body": colored_comment_body}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("Comment created successfully!")
    else:
        print(
            "Failed to create comment. Status code: ",
            f"{response.status_code}, Message: {response.text}",
        )

    return response


def set_output(name: str, value: str) -> None:
    """Set GH ENV output."""
    with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
        print(f"{name}={value}", file=fh)


def dismiss_approval(github_repo: str, issue_number: str, github_token: str) -> None:
    """Dismiss Approval."""
    url = f"https://api.github.com/repos/{github_repo}/pulls/{issue_number}/reviews"

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        reviews = response.json()
        if len(reviews) > 0:
            for review in reviews:
                if review["state"] == "APPROVED":
                    review_id = review["id"]

                    # Dismiss the approved review
                    dismiss_url = f"https://api.github.com/repos/{github_repo}/pulls/{issue_number}/reviews/{review_id}/dismissals"
                    dismiss_data = {
                        "message": "TF apply failed. Dismissing approved review.",
                    }
                    dismiss_response = requests.put(
                        dismiss_url,
                        headers=headers,
                        json=dismiss_data,
                    )

                    if dismiss_response.status_code == 200:
                        print(f"Review {review_id} dismissed successfully")
                    else:
                        print(f"Failed to dismiss review {review_id}")
                        print("Response:", dismiss_response.text)
        else:
            print("No Reviews Found")


def merge_pr(github_repo: str, issue_number: str, github_token: str) -> None:
    """Merge PR."""
    url = f"https://api.github.com/repos/{github_repo}/pulls/{issue_number}/merge"

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    commits_url = (
        f"https://api.github.com/repos/{github_repo}/pulls/{issue_number}/commits"
    )

    commit_response = requests.get(commits_url, headers=headers)
    first_commit_title = "Please give meaningful message"

    if commit_response.status_code == 200:
        commits = commit_response.json()

        if commits:
            first_commit_title = commits[0]["commit"]["message"]
            print(f"Title of the first commit: {first_commit_title}")
        else:
            print("No commits found in the pull request")
    else:
        print("Failed to fetch pull request commits")
        print("Response:", commit_response.text)

    data = {
        "commit_title": first_commit_title,  # TODO
        "commit_message": "Automatically merging after successful terraform apply",
        "merge_method": "squash",
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Pull request successfully merged")
    else:
        print("Failed to merge pull request")
        print("Response:", response.text)
