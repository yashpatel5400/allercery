"""
_name_ = is_legal.py
_authors_ = HackPrinceton 2017 Best Team
_description_ = File that checks if a food is legal
"""

"""
given a food, a list of allergies, determines if a food is okay to eat
based on the current ingredients database
returns a -1 if the food is not good to eat, a 1 if the food is good
to eat, and a 0 if the food is not in the database
"""
def is_legal(food, allergies, ingred_dict):

    if food not in ingred_dict:
        return(0)
    ingredients = ingred_dict[food]
    if any(allergies) in ingredients:
        return(-1)
    else:
        return(1)