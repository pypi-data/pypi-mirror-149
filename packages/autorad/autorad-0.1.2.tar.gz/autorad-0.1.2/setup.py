import setuptools
from setuptools import setup

with open("requirements.txt") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

test_packages = [
    "coverage==6.2",
    "great-expectations==0.14.2",
    "pytest==6.2.5",
    "hypothesis==6.36.0",
]

dev_packages = [
    "black==21.12b0",
    "flake8==4.0.1",
    "isort==5.10.1",
    "pre-commit==2.17.0",
]

webapp_packages = ["streamlit==1.2.0", "docker==5.0.3", "jupytext==1.13.8"]

docs_packages = [
    "mkdocs==1.1.2",
    "mkdocs-material==7.2.3",
    "mkdocstrings==0.15.2",
]

setup(
    name="autorad",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=required_packages,
    extras_require={
        "app": webapp_packages,
        "dev": test_packages + dev_packages + webapp_packages + docs_packages,
        "docs": docs_packages,
    },
    entry_points={
        "console_scripts": [
            "dicom_to_nifti = autorad.utils.preprocessing:dicom_app",
            "nrrd_to_nifti = autorad.utils.preprocessing:nrrd_app",
            "utils = autorad.utils.utils:app",
        ],
    },
)
