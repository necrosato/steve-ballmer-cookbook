'''
This scrip is used to test the performance of querying the database for drinks
given a list of ingredients. Takes the ingredients as arguments.
'''

import json
import sys
import argparse

def is_match(recipe, ingredients, allowed_missing):
    '''
    recipe: dict representing a recipe
    ingredients: user supplied ingredients to check against recipe ingredients.
                 dict with same keys as recipe["ingredients"]
    allowed_missing: dict with same keys as recipe["ingredients"]. Should map to ints
    '''
    misses = {}
    for key in allowed_missing:
        misses[key] = 0

    for category in recipe["ingredients"]:
        for ingredient in recipe["ingredients"][category]:
            if ingredient not in ingredients[category]:
                misses[category] += 1
                if misses[category] > allowed_missing[category]:
                    return False
    return True


def main():
    parser = argparse.ArgumentParser(description='Query the database given ingredients')
    parser.add_argument('--missing_alcohol', type=int, default=0,
                        help='Return recipes with no more than this many alcohol ingredients missing '
                             'from the supplied ingredients list.')
    parser.add_argument('--missing_garnish', type=int, default=0,
                        help='Return recipes with no more than this many garnish ingredients missing '
                             'from the supplied ingredients list.')
    parser.add_argument('--missing_mixer', type=int, default=0,
                        help='Return recipes with no more than this many mixer ingredients missing '
                             'from the supplied ingredients list.')
    parser.add_argument('--alcohol', '-a', action='append',
                        help='Alcohol ingredient to search recipes for. Can be passed multiple times.')
    parser.add_argument('--garnish', '-g', action='append',
                        help='Garnish ingredient to search recipes for. Can be passed multiple times.')
    parser.add_argument('--mixer', '-m', action='append',
                        help='Mixer ingredient to search recipes for. Can be passed multiple times.')
    args = parser.parse_args()
    alcohol = {} if args.alcohol is None else args.alcohol
    garnish = {} if args.garnish is None else args.garnish
    mixer = {} if args.mixer is None else args.mixer
    ingredients = {"alcohol": alcohol, "garnish": garnish, "mixer": mixer }
    allowed_missing = {"alcohol": args.missing_alcohol,
                       "garnish": args.missing_garnish,
                       "mixer": args.missing_mixer }
    database = json.load(open("./json/database.json", "r"))
    recipe_dict = database["recipes"]
    for recipe_name in recipe_dict:
        recipe = recipe_dict[recipe_name]
        if is_match(recipe, ingredients, allowed_missing):
            json.dump(recipe, sys.stdout, sort_keys=True, indent=4)

if __name__ == "__main__":
    main()
