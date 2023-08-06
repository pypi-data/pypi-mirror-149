import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("package_requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="TakeBlipSentimentAnalysis",
    version="0.0.1b0",
    author="Data and Analytics Research",
    author_email="analytics.dar@take.net",
    keywords='sentiment analysis',
    description="Sentiment Analysis Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True
)