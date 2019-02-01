'''
This script is meant to help build up the database. It will
go through the local page data and build json files for the database.
'''
import re
import os
import yaml
import json
from bs4 import BeautifulSoup as bs

def main():
    valid_to_html_filenames = yaml.load(open("../scrape-wiki/data/valid_links_html_filenames.yml", "r"))

    test_ingredients = ["gin", "vodka", "rum", "lemon", "whiskey"]

    database_json = {}
    # Maps ingredients to occurences
    ingredients = {}
    # List of dicts, each one representing a recipe
    recipe_list = []
    database_json["ingredients"] = ingredients
    database_json["recipes"] = recipe_list
    
    i = 0;
    for title in valid_to_html_filenames:
        json_dict = {}
        json_dict["title"] = title
        json_dict["id"] = i
        json_dict["ingredients"] = {}
        print("generating json for {}.".format(title))
        html_filename = "../scrape-wiki/" + valid_to_html_filenames[title]
        with open(html_filename, "r") as html_file:
            for j in range(3):
                ingredient = test_ingredients[(i+j)%len(test_ingredients)]
                if ingredient not in ingredients:
                    ingredients[ingredient] = 1
                else:
                    ingredients[ingredient] += 1
                json_dict["ingredients"][ingredient] = "1 oz"
            html = html_file.read()
            soup = bs(html, "html.parser")

        recipe_list.append(json_dict)
        i += 1

    json.dump(database_json, open("./json/database.json", "w"), sort_keys=True, indent=4)


if __name__ == "__main__":
    main()
