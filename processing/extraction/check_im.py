import extract
import map_ingredients as ingred
import is_legal as legal

def check_image(filename,allergies):
    database = '/Users/jeffreyregister/hackprinceton/allercery/cereal_ingredients.csv'
    ingred_dict = ingred.make_table(database)
    
    annotations = extract.get_web(filename)
    logos = extract.get_logos(filename)
    legality = []
    if annotations.web_entities:
        for entity in annotations.web_entities:
            if entity.score >= 0.5:
                legality.append(legal.is_legal(entity.description, allergies, ingred_dict))
    for logo in logos:
        legality.append(legal.is_legal(logo.description, allergies, ingred_dict))

    if sum(legality) > 0:
        if -1 in legality:
            return(0)
        else:
            return(1)
    elif sum(legality) < 0:
        if 1 in legality:
            return(0)
        else:
            return(-1)
    else:
        return(0)
