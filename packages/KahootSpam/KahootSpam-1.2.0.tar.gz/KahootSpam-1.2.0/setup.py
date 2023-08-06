import setuptools

with open("README.md", "r") as fhandle:
    long_description = fhandle.read()

setuptools.setup(
    name="KahootSpam",
    version="1.2.0",
    author="Gage Atkinson, Liam Jenne, Aedan Jones",
    author_email="someStranger87@gmail.com",
    description="A kahoot api to spam bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/someStranger8/kahoot-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)