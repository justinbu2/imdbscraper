import bs4
import os
import requests

from . import constants as const


def dump(soup, filepath):
    with open(filepath, "w") as f:
        f.write(soup.prettify())


# Unique id for a site
def lookup(site_id, site_path):
    if not os.path.isdir(const.CACHED_SITES_DIR):
        os.mkdir(const.CACHED_SITES_DIR)
    # if site_id in cache, load up the soup,
    # otherwise requests.get it and soupify it
    cachefile_path = f"{const.CACHED_SITES_DIR}/{site_id}.html"
    if os.path.exists(cachefile_path):
        with open(cachefile_path, 'r') as f:
            return bs4.BeautifulSoup(f, "html.parser")
    else:
        with open(cachefile_path, 'w') as f:
            r = requests.get(f"{const.IMDB_HOMEPAGE}/{site_path}")
            soup = bs4.BeautifulSoup(r.text, "html.parser")
        dump(soup, cachefile_path)
        return soup
