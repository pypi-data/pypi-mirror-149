"""
    seting up the package
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="basicprogressbar",
    version="1.0.0-beta",
    author="Sumiza",
    author_email="sumiza@gmail.com",
    description="Basic progress bar and discord progress bar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sumiza/basicprogressbar/",
    project_urls={
        "Bug Tracker": "https://github.com/Sumiza/basicprogressbar/issues",
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
