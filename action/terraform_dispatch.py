"""Entrypoint for Terraform-Dispatch."""

import os

import requests

from action.utils_dispatch import check_if_pr_approved, create_issue_comment, set_output

github_repo = str(os.getenv("GITHUB_REPOSITORY"))
issue_number = str(os.getenv("GITHUB_EVENT_ISSUE_NUMBER"))
github_token = str(os.getenv("INPUT_PASSED_GITHUB_TOKEN"))
pr_status = str(os.getenv("PR_STATUS"))
github_output = str(os.environ["GITHUB_OUTPUT"])
# Get the GitHub event data from the environment variable
github_event = str(os.environ.get("GITHUB_EVENT_PATH"))


url = f"https://api.github.com/repos/{github_repo}/pulls/{issue_number}"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {github_token}",
    "X-GitHub-Api-Version": "2022-11-28",
}
response = requests.get(url, headers=headers)
response_data = response.json()
# Check if the PR is against the "dev" branch
base_branch = response_data.get("base").get("ref")
print("The PR is against the branch: ", base_branch)
mergeable = response_data.get("mergeable")
mergeable_state = response_data.get("mergeable_state")
# Don't require approval if the PR is against the "dev" branch
if base_branch != "dev":
    pr_status = check_if_pr_approved(github_repo, issue_number, github_token)

else:
    # We set is as it was approved to skip the approval check
    pr_status = "approved"
print(pr_status)

if not mergeable or mergeable_state != "clean":
    set_output("apply", "NO")
    comment_body = (
        "The PR is not mergeable or status is not clean. Please check and get it clean!"
    )
    mergebale_comment_response = create_issue_comment(
        github_repo,
        issue_number,
        comment_body,
        github_token,
    )

    if mergebale_comment_response.status_code == 201:
        print("Comment created successfully!")
    else:
        print(
            "Failed to create comment. Status code: ",
            f"{mergebale_comment_response.status_code}",
            f", Message: {mergebale_comment_response.text}",
        )

elif pr_status != "approved":
    set_output("apply", "NO")
    comment_body = (
        "The PR is mergeable and status is clean but It is not APPROVED! "
        "Please have someone to review your PR"
    )
    approved_comment_response = create_issue_comment(
        github_repo,
        issue_number,
        comment_body,
        github_token,
    )
    if approved_comment_response.status_code == 201:
        print("Comment created successfully!")
    else:
        print(
            "Failed to create comment. Status code: ",
            "{approved_comment_response.status_code}, ",
            "Message: {approved_comment_response.text}",
        )

else:
    set_output("apply", "APPLY")
