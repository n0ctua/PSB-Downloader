# PSB Downloader
![version](https://img.shields.io/badge/python-3.10-blue?logo=python)

*Small python script to download a bunch of episodes from the media library of the German Public Service Broadcast (Mediathek des Öffentlich Rechtlichen Rundfunks)*

## Prerequisites
- Python >= 3.7
- [Virtualenv](https://pypi.org/project/virtualenv/)

## Setup
Setup virtual environment and install requirements:
```bash
git clone git@github.com:n0ctua/PSB-Downloader.git
  or 
git clone https://github.com/n0ctua/PSB-Downloader.git
cd PSB-Downloader

python -m venv ./venv                    
source venv/bin/activate
python -m pip install -r requirements.txt
```
Change `config.ini` to your needs:

```
title = title of TV program you want to download
download_since = download episodes released from this date until today
dl_dir = directory where files will be downloaded to
```

## Usage
```bash
python main.py [-h] [-d] [-n] [-q]

options:
  -h, --help       show this help message and exit
  -d, --dry-run    only show what would be downloaded, without actually doing anything
  -n, --no-update  don't update the date in config.ini to the current date after the download finished
  -q, --quiet      don't output information to STDOUT
```
