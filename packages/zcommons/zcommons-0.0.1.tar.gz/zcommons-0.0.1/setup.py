import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="zcommons",
    version="0.0.1",
    author="malanore.z",
    author_email="malanore.z@gmail.com",
    description="A collection of common utils for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/malanore-z/zcommons4p",
    project_urls={
        "Bug Tracker": "https://github.com/malanore-z/zcommons4p/issues",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    package_dir={"": "src"},
    packages=["zcommons"],
    include_package_data=True,
    install_requires=[
        "dataclasses;python_version<'3.7'"
    ]
)
