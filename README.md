# Terraform CI/CD (GCP)

This repository provides a streamlined approach to manage Terraform CI/CD pipelines for projects hosted on Google Cloud Platform (GCP). With this setup, you can use GitHub Actions to automate Terraform plan and apply processes in a multi-branch environment.

## How to Use

### 1. Terraform Plan

Create a Terraform plan GitHub Action by adding the following configuration to `.github/workflows/plan.yaml`. This setup enables a multi-branch approach to manage different environments (e.g., `dev`, `stage`, `prod`).

```yaml
name: Terraform Plan

on:
  pull_request:
    branches:
      - stage
      - prod
      - dev

permissions: write-all

jobs:
  plan:
    uses: ffernandez92/terraform-cicd/.github/workflows/plan.yaml@main
    with:
      dev-project-number: 123456789011
      stage-project-number: 123456789012
      prod-project-number: 123456789013
      dev-project-name: my-dev-project
      stage-project-name: my-stage-project
      prod-project-name: my-prod-project
      stage-branches: stage
      prod-branches: prod
      dev-branches: dev
```

### 2. Terraform Apply

To apply Terraform changes, follow these steps:

1. Ensure your pull request (PR) is approved.
2. Add a comment to the PR with the message `terraform apply`.

Add the following configuration to `.github/workflows/apply.yaml` to enable the apply process:

```yaml
name: Terraform Apply

on: issue_comment

permissions: write-all

jobs:
  apply:
    uses: ffernandez92/terraform-cicd/.github/workflows/apply.yaml@main
    with:
      dev-project-number: 123456789011
      stage-project-number: 123456789012
      prod-project-number: 123456789013
      dev-project-name: my-dev-project
      stage-project-name: my-stage-project
      prod-project-name: my-prod-project
      stage-branches: stage
      prod-branches: prod
      dev-branches: dev
```

### Notes:
- Replace the project numbers (`123456789011`, etc.) and project names (`my-dev-project`, etc.) with your actual GCP project details.
- Adjust the branch names (`dev`, `stage`, `prod`) based on your branching strategy.
- 

### Features:
- **Multi-Branch Support:** Automatically triggers Terraform plan and apply for specific branches.
- **Approval Workflow:** Requires PR approval and a specific comment to apply changes, ensuring controlled deployments.
- **Customizable Configuration:** Easily adapt to your project structure by modifying input parameters.

### Additional Information:
- This setup uses **Google Cloud Workload Identity** for secure and seamless authentication. Check [here](https://cloud.google.com/blog/products/identity-security/enabling-keyless-authentication-from-github-actions) how to setup. 
