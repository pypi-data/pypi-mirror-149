# Evaluate
Evaluate is a script that can be run to gather information about projects from a gitlab self-managed instance. This information is useful to the GitLab Professional Services (PS) team to accurately scope migration services. 

## Use Case
GitLab PS plans to share this script with a Customer to run against their self managed instance. Then the customer can send back the output files to enable GitLab engagement managers to scope engagements accurately. 

## Install

```
pip install gitlab-evaluate
```

## Usage

### System level data gathering
Evaluate is meant to be run by an administrator of a GitLab Self Managed deployment to gather data about every project on the instance. 

1. A GitLab system administrator should  [provision an access token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#create-a-personal-access-token)
1. Then, after installing `gitlab-evaluate` from the [Install](#install) section above,
1. Run :point_down: 

```bash
# For evaluating a GitLab instance
evaluate-gitlab -t <access-token-with-api-admin-privileges> -s https://gitlab.example.com
```
1. This should create a file called `evaluate_output.csv`
1. If you're coordinating a GitLab Professional Services engageemnt, email this file to the GitLab account team. 

### To gather CI data from a single repo

```bash
# For evaluating a single git repo's CI readiness
evaluate-ci-readiness -r|--repo <git-repo-url>
```

### Command help screen

```
usage: evaluate-gitlab [-h] [-t TOKEN] [-s SOURCE] [-f FILENAME] [-o] [-i] [-p PROCESSES]

optional arguments:
  -h, --help            show this help message and exit
  -t TOKEN, --token TOKEN
                        Personal Access Token: REQ'd
  -s SOURCE, --source SOURCE
                        Source URL: REQ'd
  -f FILENAME, --filename FILENAME
                        CSV Output File Name. If not set, will default to 'evaluate_output.csv'
  -o, --output          Output Per Project Stats to screen
  -i, --insecure        Set to ignore SSL warnings.
  -p PROCESSES, --processes PROCESSES
                        Number of processes. Defaults to number of CPU cores
```

```
usage: evaluate-ci-readiness [-h] [-r REPO]

optional arguments:
  -h, --help            show this help message and exit
  -r REPO, --repo REPO  Git Repository To Clone (ex: https://username:password@repo.com
```

## Using a docker container

[Docker containers with evaluate installed](https://gitlab.com/gitlab-org/professional-services-automation/tools/utilities/evaluate/container_registry) are also available to use.

### Local usage

```bash
# Spin up container
docker run --name evaluate -it registry.gitlab.com/gitlab-org/professional-services-automation/tools/utilities/evaluate:latest /bin/bash

# In docker shell
evaluate-ci-readiness -r|--repo <git-repo-url>
evaluate-gitlab -t <access-token-with-api-admin-privileges> -s https://gitlab.example.com
```

### Example GitLab CI job using evaluate ci readiness script

```yaml
evaluate node-js:
  stage: test
  script:
    - evaluate-ci-readiness --repo=https://github.com/nodejs/node.git
  artifacts:
    paths:
      - node.csv
```

To **test**, consider standing up local docker container of gitlab. Provision a personal access token of a user who has system admin priviledges. Create multiple projects with varying number of commits, pipelines, merge requests, issues. Consider importing an open source repo or using [GPT](https://gitlab.com/gitlab-org/quality/performance) to add projects to the system.  

## Design
Design for the script can be found [here](https://gitlab.com/gitlab-com/customer-success/professional-services-group/ps-leadership-team/ps-practice-management/-/issues/83)

## Project Thresholds
_Below are the thresholds we will use to determine whether a project can be considered for normal migration or needs to have special steps taken in order to migrate_ 

### Project Data
- Pipelines - 1,500 max
- Issues - 1,500 total (not just open)
- Merge Requests - 1,500 total (not just merged)
- Container images - 20GB per project
- Packages - Any packages present

### Repo Data
- commits - 20K
- branches - 1K
- tags - 1K
- Disk Size - 10GB
