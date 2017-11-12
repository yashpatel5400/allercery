"""
_name_ = map_ingredients.py
_authors_ = HackPrinceton 2017 Best Team
_description_ = File that makes a dictionary of the foods and ingredients from our database
"""

# makes a dictionary of the foods and ingredients in a given csv database
def make_table(database):

    cereal = []
    brand = []
    ingred = []
    with open(database,'r') as fid:
        lines = fid.readlines()
    for i in range(1,len(lines)):
        about = lines[i].strip('\n').split(';')
        cereal.append(about[0])
        brand.append(about[1])
        ingredients = about[2].lower()
        ingred.append(set(ingredients.split(', ')))

    ingred_dict = dict(zip(cereal,ingred))

    return(ingred_dict)
