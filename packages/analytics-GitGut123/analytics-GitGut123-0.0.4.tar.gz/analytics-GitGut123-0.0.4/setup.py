"""Setup script for setuptools to build the package analytics-GitGut123."""
import setuptools

setuptools.setup(
    name="analytics-GitGut123",
    version="0.0.4",
    author="Peter",
    author_email="author@example.com",
    description="A small example package",
    long_description="This is a very long description",
    long_description_content_type="text/markdown",
    url="https://github.com/GitGut123/dataeng_exercise",
    project_urls={
        "Bug Tracker": "https://github.com/datafoundationcmc/dataeng_exercise/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
