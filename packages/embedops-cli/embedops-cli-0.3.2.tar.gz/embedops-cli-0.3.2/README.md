# EmbedOps Tools
Collection of tools to support the embedops.io platform. 

## File structure

- eotools -- code for utilities to be used by local_cli, remote_ci, or future tools. 
- api -- wrapper for the API calls to embedops.io and future integrated tools
- docs -- documentation
- [embedops_cli](embedops_cli/README.md) -- code specifically for the CLI user experience
- tests -- unit tests for all code


# embedops-cli

- CLI tool to enable local runs of BitBucket and GitLab CI jobs in Docker
- More information can be found in the [CLI architecture document](docs/CLI-architecture.md)

## For Developers
Releases and Tag Policy:
- When merging into the main branch, or want to push to the releases, add a tag and it will build and deploy a new release
- Tags should begin with `cli-`

## For Users

### GitHub

Auto-detection of the GitHub CI configuration file works only if there is one file in the .github/workflows directory. When there are more than one files in that directory, use the --filename flag to specify a GitHub CI configuration.

Syntax:

```bash
embedops-cli jobs --filename <PATH_TO_CI_CONFIG_FILE> run <JOB_NAME>
```

# eotools

- EmbedOps Docker image so all CI jobs will have access to the CI tools to send info to the EmbedOps backend
- Tools are intended to be primarily used via the Dockerfile discussed below

## Limitations
- `armsize` or equivalent command needs to be run explicitly from the toolchain or the yaml file. 

# EmbedOps Dockerfiles
EmbedOps Docker Tools are added on top of D5 built containers to ensure they are able to send information to the embedops.io backend.

[Suppported Images Status Table](https://docs.google.com/spreadsheets/d/1U7-xEpzgdDhnvMBWvhvC9FOapJrSsvjuOuV7XGS-p_8/edit?usp=sharing)

## For Developers
The containers are divided into the main container and a development container.
- If working on a feature branch, do not add a tag to your branch so your changes are pushed to the development container. The SHA will be used as the tag.
- When merging into the main branch, or want to push to the main container, add a tag and it will update the :latest tag as well as add the tag you originally added
- Tags should begin with `docker-`

# Test Plan
We will be using Pytest in this project. Unit tests for Python shall reside in the `tests` directory
To ensure Pytest can discover the tests, and to keep consistency:
- The test files should be named in the pattern `<source_filename>_test.py`. 
- The test cases themselves should have the pattern `def test_<test_name>():`

Info about functional testing can be found in [Functional Test Plan](docs/FunctionalTestPlan.md)

# General Info

[CI Terminology Dictionary](https://docs.google.com/spreadsheets/d/1Cf83XBiZAC5vDKK8OJwGMCItwwwITHLpXmigSfrmy1s/edit#gid=0)

## License
Copyright 2021 Dojo Five, LLC

## Code Owners

- [Dojo Five](https://dojofive.com/)  
    Engineers:
    - Bailey Steinfadt
    - Bryan Siepert
    - Zhi Xuen Lai
    - Aaron Fontaine

    Former Engineers: 
    - Cole Spear

