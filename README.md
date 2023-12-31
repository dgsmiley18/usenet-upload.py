# usenet-upload.py

Crude and simple script to upload `.mkv` files in a given directory.

## Features
- Generates `par2` files for each `.mkv`
- Can move the files into their own folders, 
- Can move the files into their own folders and it passes the `.mkv` file along with it's corresponding `.par2` files directly to Nyuu via CLI
- Looks into subdirectories for `.mkv` files
- Probably has alot of cases where it breaks. Worked on my machine in my limited testing
- Someone please make a better script I can't code

## Prerequisites
- [Python 3.11](https://www.python.org/downloads/)
- [animetosho/Nyuu@a4b1712](https://github.com/animetosho/Nyuu/commit/a4b1712d77faeacaae114c966c238773acc534fb) - You need this version or newer. [v0.4.1 is outdated and you shouldn't use it](https://github.com/animetosho/Nyuu/releases/tag/v0.4.1).
- [animetosho/ParPar](https://github.com/animetosho/ParPar)

## Usage

Before you can use this, you have the edit and rename example-config to config [example-config.json](https://github.com/cannibalChipper/usenet-upload.py/blob/main/example-config.json).

### Windows
```
usenet-upload.py path\to\directory\with\mkv\files
```
```
py usenet-upload.py path\to\directory\with\mkv\files
```

### Linux
```
python3 usenet-upload.py path/to/directory/with/mkv/files
```

### help

```
> usenet-upload.py --help
usage: usenet-upload.py [-h] [-p] [-n] [-m] path

A script for uploading MKV files to usenet

positional arguments:
  path          Path to directory containing .mkv files

options:
  -h, --help    show this help message and exit
  -p, --parpar  Only run Parpar
  -n, --nyuu    Only run Nyuu
  -m, --move    Move files into their own folders
```
