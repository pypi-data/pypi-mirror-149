import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tessa-pretty-help", 
    version="0.0.4",
    author="Prakarsh17",
    author_email="pranjal.prakarsh@outlook.com",
    description="An embed version of the built in help command for discord.py and probably other forks of discord.py Inspired by the DefaultHelpCommand that discord.py uses, but revised for embeds and additional sorting on individual pages that can be scrolled through with reactions.. An improved version of discord-pretty-help",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url="https://github.com/prakarsh17/tessa-pretty-help",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)