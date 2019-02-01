'''
This script is meant to help build up the data for the drinks database. It will
go through the local page data and attempt to discern actual cocktail recipes
from other pages.
'''
import requests
import re
import os
import yaml
from bs4 import BeautifulSoup as bs

def main():
    valid_to_html_filenames = {}
    not_valid_to_html_filenames = {}
    all_to_html_filenames = yaml.load(open("./data/all_links_html_filenames.yml", "r"))
    
    must_contain = ["Commonly used ingredients"]
    for title in all_to_html_filenames:
        html_filename = all_to_html_filenames[title]
        valid = False
        # any page with "(cocktail)" in the title is definitely a valid link
        if "(cocktail)" in title:
            valid = True
        else:
            with open(html_filename, "r") as html_file:
                html = html_file.read()
                soup = bs(html, "html.parser")
                # Check for phrases in the html to determine if its a recipe
                for phrase in must_contain:
                    if phrase in html:
                        valid = True
                        break

        if valid:
            print('"{}" ({}) is a valid link.'.format(title, html_filename))
            valid_to_html_filenames[title] = html_filename
        else:
            print('"{}" ({}) is not a valid link.'.format(title, html_filename))
            not_valid_to_html_filenames[title] = html_filename

    print("number of valid links : {}".format(len(valid_to_html_filenames)))
    print("number of not valid links : {}".format(len(not_valid_to_html_filenames)))

    with open("./data/valid_links_html_filenames.yml", "w") as valid_links_html_filenames:
        yaml.dump(valid_to_html_filenames, valid_links_html_filenames, default_flow_style=False)

    with open("./data/not_valid_links_html_filenames.yml", "w") as not_valid_links_html_filenames:
        yaml.dump(not_valid_to_html_filenames, not_valid_links_html_filenames, default_flow_style=False)


if __name__ == "__main__":
    main()
