"""Beginning the Terraform apply."""

import os

from utils_dispatch import create_issue_comment

github_repo = str(os.getenv("GITHUB_REPOSITORY"))
issue_number = str(os.getenv("GITHUB_EVENT_ISSUE_NUMBER"))
github_token = str(os.getenv("INPUT_PASSED_GITHUB_TOKEN"))
github_run_id = str(os.getenv("GITHUB_RUN_ID"))

actions_link = f"https://github.com/{github_repo}/actions/runs/{github_run_id}"
comment_body = f"Terraform dispatch and apply begins. Checkout here: {actions_link}"
response = create_issue_comment(github_repo, issue_number, comment_body, github_token)
