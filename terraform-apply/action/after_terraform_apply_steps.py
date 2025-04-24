"""Steps for what occurs AFTER apply."""

import os

from action.utils_apply import (
    create_issue_comment,
    dismiss_approval,
    merge_pr,
    set_output,
)

github_repo = str(os.getenv("GITHUB_REPOSITORY"))
issue_number = str(os.getenv("GITHUB_EVENT_ISSUE_NUMBER"))
github_token = str(os.getenv("INPUT_PASSED_GITHUB_TOKEN"))
terrafrom_error = str(os.getenv("TERRAFROM_ERROR"))
terraform_apply_failed = str(os.getenv("TERRAFORM_APPLY_FAILED"))

comment_body = terrafrom_error
apply_response = create_issue_comment(
    github_repo,
    issue_number,
    comment_body,
    github_token,
)

print(terraform_apply_failed)

if terraform_apply_failed == "true":
    set_output("apply_done", "false")
    dismiss_approval(github_repo, issue_number, github_token)
else:
    set_output("apply_done", "true")  # not needed but leave it for now.
    merge_pr(github_repo, issue_number, github_token)
