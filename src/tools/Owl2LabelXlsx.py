from bs4 import BeautifulSoup as bs
import lxml
import json
import pandas as pd

GLOBAL_URI = "http://www.semanticweb.org/ika/vvmethods/cruise/"
SCENARIO_PREFIX = "sce#"
CONCEPT_PREFIX = "con#"

def main():
    bs_owl = get_owl("cruise.owl")
    classes_dict = create_table(bs_owl)

    with open('cruise_reduced.json', 'w') as fp:
        json.dump(classes_dict, fp, indent=4, ensure_ascii=False)

    classes_dict = reduce_lists(classes_dict)
    classes_df = pd.DataFrame.from_dict(classes_dict)
    classes_df = classes_df.fillna('')

    classes_df.to_excel("criuse_reduced.xlsx")

    print(classes_df)


def get_owl(filename):
    with open(filename, encoding='utf-8') as owl_file:
        owl_content = owl_file.readlines()
        owl_content = "".join(owl_content)
        bs_owl = bs(owl_content, features="xml", from_encoding="utf-8")
        return bs_owl


def create_table(owl_data):
    owl_classes = owl_data.find_all("owl:Class")
    
    class_list = []

    for owl_class in owl_classes:
        class_list.append(process_class(owl_class))

    return class_list


def process_class(class_tag):  
    class_dict = {}
    class_dict["IRI"] = class_tag.get("rdf:about").removeprefix(GLOBAL_URI+SCENARIO_PREFIX)

    # Process labels
    labels = class_tag.find_all("rdfs:label")

    for label in labels:
        if label.get("xml:lang")=="de":
            class_dict["label_DE"] = label.text
        elif label.get("xml:lang")=="en":
            class_dict["label_EN"] = label.text
    
    # Process superclasses
    superclasses = class_tag.find_all("rdfs:subClassOf")
    class_dict["superclasses"] = []

    for sc in superclasses:
        if sc.findChild("owl:Restriction"):
            continue

        class_dict["superclasses"].append(sc.get("rdf:resource").removeprefix(GLOBAL_URI+SCENARIO_PREFIX))
    
    return class_dict

def reduce_lists(class_list):
    for c in class_list:
        c["superclasses"] = ";".join(c["superclasses"])
    return class_list
    



if __name__ == "__main__":
    main()
