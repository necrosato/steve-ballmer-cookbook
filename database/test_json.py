'''
This scrip is used to test the performance of querying the database for drinks
given a list of ingredients. Takes the ingredients as arguments.
'''

import json
import sys

def main():
    database_list = json.load(open("./json/database.json", "r"))
    query_ingredients = sys.argv[1:]
    for entry in database_list:
        match = True
        for ingredient in query_ingredients:
            if ingredient not in entry["ingredients"]:
                match = False
                break
        if match:
            json.dump(entry, sys.stdout, sort_keys=True, indent=4)

if __name__ == "__main__":
    main()
