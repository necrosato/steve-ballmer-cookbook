'''
This script is meant to help build up the data for the drinks database.  I lack
the means to do sufficient parsing of the html, currently. It will be much quicker to
operate on local data so I'm just going to be downloading the raw html and
creating manifests of them.
'''
import requests
import re
import os
import yaml
from bs4 import BeautifulSoup as bs

def main():
    valid_to_url = {}
    valid_to_html_filenames = {}
    not_valid_to_url = {}
    not_valid_to_html_filenames = {}
    all_to_url = {}
    all_to_html_filenames = {}
    
    must_contain = ["Commonly used ingredients"]
    list_of_cocktails = requests.get("https://en.wikipedia.org/wiki/List_of_cocktails")
    loc_soup = bs(list_of_cocktails.text, 'html.parser')
    # Look at every wiki link in the main page
    i = 0
    for link in loc_soup.findAll('a', attrs={'href': re.compile("^/wiki/")}):
        url = 'https://en.wikipedia.org' + link.get('href')
        if "jpg" in url:
            continue
        link_request = requests.get(url)
        link_soup = bs(link_request.text, 'html.parser')
        title = link_soup.find("title").text
        html_filename = "./data/html/{:04d}.html".format(i)
        html = link_soup.prettify()

        all_to_url[title] = url
        all_to_html_filenames[title] = html_filename
        with open(html_filename, "w") as html_file:
            html_file.write(html)

        # Check for phrases in the html to determine if its a recipe
        valid = True
        for phrase in must_contain:
            if phrase not in html:
                print('{} is not a valid recipe. It does not contain the phrase "{}"'.format(
                    title, phrase))
                valid = False

        if not valid:
            not_valid_to_url[title] = url
            not_valid_to_html_filenames[title] = html_filename
        else:
            print(title + " is a valid recipe")
            valid_to_url[title] = url
            valid_to_html_filenames[title] = html_filename
        i+=1

    with open("./data/all_links.yml", "w") as all_links:
        yaml.dump(all_to_url, all_links, default_flow_style=False)
    with open("./data/all_links_html_filenames.yml", "w") as all_links_html_filenames:
        yaml.dump(all_to_html_filenames, all_links_html_filenames, default_flow_style=False)

    with open("./data/valid_links.yml", "w") as valid_links:
        yaml.dump(valid_to_url, valid_links, default_flow_style=False)
    with open("./data/valid_links_html_filenames.yml", "w") as valid_links_html_filenames:
        yaml.dump(valid_to_html_filenames, valid_links_html_filenames, default_flow_style=False)

    with open("./data/not_valid_links.yml", "w") as not_valid_links:
        yaml.dump(not_valid_to_url, not_valid_links, default_flow_style=False)
    with open("./data/not_valid_links_html_filenames.yml", "w") as not_valid_links_html_filenames:
        yaml.dump(not_valid_to_html_filenames, not_valid_links_html_filenames, default_flow_style=False)


if __name__ == "__main__":
    main()
