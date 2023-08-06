import setuptools
import subprocess
import os

version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OpenGround-SDK",
    version=version,
    author="Bentley Systems Ltd",
    author_email="support@bentley.com",
    description="OpenGround SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BentleySystems/OpenGround-SDK-Python",        
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",    
    package_data={'': ['*.html']},
)