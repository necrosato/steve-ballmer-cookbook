'''
This script is meant to help build up the data for the drinks database. It will
download all links in the main page (not jpgs) as html and create a map of page
title to html, and a map of page title to url.
'''

import requests
import re
import os
import yaml
from bs4 import BeautifulSoup as bs

def main():
    name_to_url = {}
    name_to_html_filenames = {}
    
    loc_request = requests.get("https://en.wikipedia.org/wiki/List_of_cocktails")
    loc_soup = bs(loc_request.text, 'html.parser')
    # Look at every wiki link in the main page
    i = 0
    for link in loc_soup.findAll('a', attrs={'href': re.compile("^/wiki/")}):
        url = 'https://en.wikipedia.org' + link.get('href')
        if "jpg" in url:
            continue
        print("Scraping {} (link number {})".format(url, i));
        link_request = requests.get(url)
        link_soup = bs(link_request.text, 'html.parser')
        title = link_soup.find("title").text.replace(" - Wikipedia", "")
        html_filename = "./data/html/{:04d}.html".format(i)
        html = link_soup.prettify()

        if title not in name_to_url:
            name_to_url[title] = url
            name_to_html_filenames[title] = html_filename
            with open(html_filename, "w") as html_file:
                html_file.write(html)
            i+=1

    with open("./data/name_to_links.yml", "w") as all_links:
        yaml.dump(name_to_url, all_links, default_flow_style=False)
    with open("./data/name_to_html_filenames.yml", "w") as all_links_html_filenames:
        yaml.dump(name_to_html_filenames, all_links_html_filenames, default_flow_style=False)

if __name__ == "__main__":
    main()
