# Manga Tracker

## Overview
Manga Tracker (or ```mantrack```) is a lightweight CLI program to track your favorite manga updates. Its core process is web-crawling and represent better visual of data representation in command line. You can start tracking process, update your list of target manga, and even configure the system directly by simple CLI. ```mantrack``` also has great scalability with multi-website multi-target manga while keep maintaining safe and server-friendly web-crawling procedure.


## Requirements
- Python >= 3.6

## Install
First, clone this project:
```sh
git clone https://github.com/avidito/manga_tracker.git
```

Then create virtualenv and activate it (this is recommended approach to isolate ```mantrack```):
```sh
virtualenv venv
.\venv\Scripts\activate
```

After that, go to project root directory and install ```mantrack```:
```sh
pip install --editable .
```

## Documentation
To show project help, run this command:
```sh
mantrack --help
```

## Resources
- [Click Official Documentation](https://click.palletsprojects.com/en/7.x/)
- [Building A Registration CLI with Python and CLICK](https://www.youtube.com/watch?v=KEHJscp2DW0) by [JCharisTech & J-Secur1ty](https://www.youtube.com/channel/UC2wMHF4HBkTMGLsvZAIWzRg)
- [Packaging Click Project with Setuptools](https://github.com/pallets/click/blob/master/docs/setuptools.rst#scripts-in-packages)
- [Setup.py Sample](https://github.com/pypa/sampleproject/blob/main/setup.py)
