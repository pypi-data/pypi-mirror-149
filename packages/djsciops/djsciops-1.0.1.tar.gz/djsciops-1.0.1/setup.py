import setuptools
import pathlib
import djsciops as package
import re

here = pathlib.Path(__file__).parent.resolve()
with open(pathlib.Path(here, "pip_requirements.txt")) as f:
    requirements = [
        "{pkg} @ {target}#egg={pkg}".format(
            pkg=re.search(r"/([A-Za-z0-9\-]+)\.git", r).group(1), target=r
        )
        if "+" in r
        else r
        for r in f.read().splitlines()
        if "#" not in r
    ]

setuptools.setup(
    name=package.__name__,
    version=package.__version__,
    author="DataJoint",
    author_email="djbot@datajoint.io",
    description="A suite of customer CLI tools for DataJoint SciOps.",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/dj-sciops/djsciops-python",
    packages=setuptools.find_packages(exclude=["tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            f"{package.__name__}={package.__name__}.command_line:{package.__name__}"
        ],
    },
    install_requires=requirements,
)
