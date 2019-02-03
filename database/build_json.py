'''
This script is meant to help build up the database. It will
go through the local page data and build json files for the database.
'''
import re
import os
import yaml
import json
import webbrowser
from bs4 import BeautifulSoup as bs

def get_ingredients_count(recipes):
    ingredients = {}
    for title in recipes:
        recipe = recipes[title]
        for category in recipe["ingredients"]:
            if category not in ingredients:
                ingredients[category] = {}
            for ingredient in recipe["ingredients"][category]:
                if ingredient not in ingredients[category]:
                    ingredients[category][ingredient] = 1
                else:
                    ingredients[category][ingredient] += 1
    return ingredients


def get_procedure():
    steps = []
    sentences = input("enter steps: ")
    for sentence in sentences.split('.'):
        if sentence.strip() is not '':
            steps.append(sentence.strip() + '.')
    return steps
    

def get_ingredients():
    ingredients = { "alcohol": {}, "mixer": {}, "garnish": {} }
    # populate ingredients
    for category in sorted(ingredients):
        print("Getting ingredients for category '{}'".format(category))
        ingredient_name = input("enter {} ingredient name for recipe (lower case), "
                                "enter nothing to move on: ".format(category))
        while ingredient_name is not '':
            ingredient = {}
            amount = input("enter amount, (float only, no unit): ")
            is_float = False
            while not is_float:
                try:
                    ingredient["amount"] = float(amount)
                    is_float = True
                except:
                    amount = input("amount must just be a float (e.g. 1.5, not 1 1/2, etc), please re-enter: ")
            unit = input("enter unit (lower case): ")
            ingredient["unit"] = unit
            ingredients[category][ingredient_name] = ingredient
            ingredient_name = input("enter {} ingredient name for recipe (lower case), "
                                    "enter nothing to move on: ".format(category))
    return ingredients


def main():
    valid_to_html_filenames = yaml.load(open("../scrape-wiki/data/valid_links_html_filenames.yml", "r"))
    name_to_url = yaml.load(open("../scrape-wiki/data/name_to_links.yml", "r"))

    db_path = "./json/database.json"
    if os.path.isfile(db_path):
        database_json = yaml.load(open("./json/database.json", "r"))
    else:
        # Maps ingredients to occurences
        # dict of dicts, name to a recipe
        database_json = {}
        database_json["recipes"] = {}
    
    try:
        for title in sorted(valid_to_html_filenames):
            if title not in database_json["recipes"]:
                print("generating json for {}.".format(title))
                recipe = {}
                html_filename = "../scrape-wiki/" + valid_to_html_filenames[title]
                recipe["html_file"] = html_filename
                recipe["id"] = int(html_filename[-9:-5])
                recipe["url"] = name_to_url[title]
                webbrowser.open(recipe["url"], new=2)
                ok = 'y'
                while ok is 'y':
                    recipe["ingredients"] = get_ingredients()
                    ok = input("redo? 'y' to redo, enter nothing to move on: ")
                # List of strings that are steps
                ok = 'y'
                while ok is 'y':
                    recipe["procedure"] = get_procedure()
                    ok = input("redo? 'y' to redo, enter nothing to move on: ")
                database_json["recipes"][title] = recipe
            else:
                print("Skipping '{}' since it is in the database".format(title))
    except:
        print("\nSaving progress...")

    print("counting ingredients in recipes")
    database_json["ingredients"] = get_ingredients_count(database_json["recipes"])
    print("saving database to file")
    json.dump(database_json, open(db_path, "w"), sort_keys=True, indent=4)


if __name__ == "__main__":
    main()
