import argparse
import configparser
import dateparser
import datetime as dt
import logging
import os
import re
import requests
import shutil
import sys

from bs4 import BeautifulSoup

config = configparser.ConfigParser()
configfile_name = 'config.ini'

parser = argparse.ArgumentParser(description='Download a list of episodes from the media library of the German PSB')
parser.add_argument('-c', '--cronjob', action='store_true', help='use this option if you run this script via cron')
parser.add_argument('-d', '--dry-run', action='store_true', help='only show what would be downloaded, '
                                                                 'without actually doing anything')
parser.add_argument('-n', '--no-update', action='store_true', help='don\'t update the date in config.ini to the '
                                                                   'current date after the download finished')
parser.add_argument('-q', '--quiet', action='store_true', help='don\'t output information to STDOUT')
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.WARNING if args.quiet else logging.INFO)


def download_list(soup, title, download_since):
    dl_list = []
    for item in soup.find_all('title', string=title):
        episode_date = dateparser.parse(item.parent.pubDate.string)
        if episode_date <= download_since:
            break
        dl_list.append((item.string, item.parent.link.string))
    return dl_list


def download_file(filename, directory, url):
    path = f'{directory}/{filename.replace(" ", "_")}.mp4'
    with requests.get(url, stream=True) as r:
        with open(path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def read_config():
    # Check if there is already a configurtion file
    if not os.path.isfile(configfile_name):
        # Create the configuration file as it doesn't exist yet
        config['DEFAULT'] = {
            'feed_url': 'https://mediathekviewweb.de/feed',
            'title': 'ZDF Magazin Royale',
            'download_since': dt.datetime.now(dt.timezone.utc).isoformat(),
            'dl_dir':  '.',
        }
        with open(configfile_name, 'w') as configfile:
            config.write(configfile)
    else:
        config.read('config.ini')


if __name__ == '__main__':
    if args.cronjob:
        os.chdir(os.path.dirname(sys.argv[0]))
    read_config()
    conf = config['DEFAULT']
    payload = {'query': conf['title']}
    title = re.compile('^' + conf['title'])
    download_since = dt.datetime.fromisoformat(conf['download_since'])

    page = requests.get(conf['feed_url'], params=payload)
    soup = BeautifulSoup(page.text, 'xml')
    dl_list = download_list(soup, title, download_since)

    if dl_list:
        for count, (dl_title, dl_url) in enumerate(dl_list, start=1):
            if args.dry_run:
                logging.info(f'dry run: Would download episode [{count}/{len(dl_list)}] "{dl_title}"... ')
            else:
                logging.info(f'Downloading episode  [{count}/{len(dl_list)}] "{dl_title}"... ')
                download_file(dl_title, conf['dl_dir'], dl_url)
                logging.info('done')
    else:
        logging.info('Download list is empty. Nothing to do...')
        exit(0)

    if not args.dry_run and not args.no_update:
        config['DEFAULT']['download_since'] = dt.datetime.now(dt.timezone.utc).isoformat()
        with open(configfile_name, 'w') as configfile:
            config.write(configfile)

