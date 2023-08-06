import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


def parse_tag(tag_name):
    if "v" == tag_name[0]:
        return tag_name[1:]
    else:
        return tag_name


if os.environ.get("CI_COMMIT_TAG"):
    version = parse_tag(os.environ["CI_COMMIT_TAG"])
elif os.environ.get("CI_JOB_ID"):
    job_id = os.environ["CI_JOB_ID"]
    version = job_id
else:
    # get latest git tag
    cmd = "git describe --tags --abbrev=0"
    stream = os.popen(cmd)
    latest_tag = stream.read().rstrip()
    latest_version = parse_tag(latest_tag)
    version = f"{latest_version}"


setuptools.setup(
    name="optimaldesign",
    version=version,
    author="Markus Unkel",
    author_email="markus@unkel.io",
    description="OptimalDesign",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/maunke/optimaldesign",
    packages=setuptools.find_packages(),
    setup_requires=["better-setuptools-git-version", "wheel", "pytest-runner"],
    license="MIT",
    install_requires=requirements,
    tests_require=["pytest", "pytest-cov", "coverage"],
    test_suite="tests",
)
