# picorg
[![Build Status](https://img.shields.io/pypi/v/picorg.svg?style=flat)](https://img.shields.io/pypi/v/picorg.svg?style=flat)
[![Build Status](https://img.shields.io/github/license/frangiz/picorg.svg)](https://img.shields.io/github/license/frangiz/picorg.svg)
[![codecov](https://codecov.io/gh/frangiz/picorg/branch/master/graph/badge.svg?token=D8VG9ENXZ7)](https://codecov.io/gh/frangiz/picorg)

A set of scripts to organize pictures. It is ideal if you save your images in different locations on your hard drives and manually backup your images from your phone.

## Installation
```python
pip install picorg
```

## Usage
```python
# Renames all images in the current working directory and its subdirectories. It tries to use the timestamp of when the image was taken from the EXIF data. If the script cannot find a suitable name for a file, it will be moved to a **NOK** folder and the filename will be printed to the console.
picorg -a rename

# Checks all files in current working dir for files with the same content. If two files has the same content,
# the one with the "biggest" name is moved to a *duplicates* folder. It then traverses all the files in
# all the directories listed in pic_paths (in the settings file). If a file matches by name and content,
# the file in current working dir will be moved to the *duplicates* folder.
picorg -a duplicates
```

## Configuration
A settings file is created in <USER_HOME>/.picorg that stores the users settings.

## Developing
Install dependencies from the requirements.txt file
```python
pip install -r requirements.txt
```

Create a package and install with
```python
python -m build
pip install -e .
```

### Before commit
Run the command `pre-commit run --verbose --all-files --show-diff-on-failure` before any commits on order to be consistent with formatting and having sorted imports.

## Creating a new version.
* Create a new tag and push. The publishing of the new version is done automagically.