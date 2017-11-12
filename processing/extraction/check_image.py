import processing.extraction.extract as extract
import processing.extraction.map_ingredients as ingred
import processing.extraction.is_legal as legal
import processing.extraction.settings as s

def check_image(filename,allergies):
    ingred_dict = ingred.make_table(s.DB)
    
    annotations = extract.get_web(filename)
    logos = extract.get_logos(filename)
    legality = []
    if len(logos) > 0:
        for logo in logos:
            legality.append(legal.is_legal(logo.description, allergies, ingred_dict))
    else:
        if annotations.web_entities:
            for entity in annotations.web_entities:
                if entity.score >= 0.5:
                    legality.append(legal.is_legal(entity.description, allergies, ingred_dict))

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
