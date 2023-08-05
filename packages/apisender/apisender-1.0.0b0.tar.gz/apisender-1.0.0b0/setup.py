"""
    setting up the package
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apisender",
    version="1.0.0-beta",
    author="Sumiza",
    author_email="sumiza@gmail.com",
    description="Sends messages to various APIs for email or discord",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sumiza/apisender/",
    project_urls={
        "Bug Tracker": "https://github.com/Sumiza/apisender/issues",
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
    install_requires=["requests"]
)
