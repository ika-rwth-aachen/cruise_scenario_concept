from bs4 import BeautifulSoup as bs
import lxml
import json
import pandas as pd

GLOBAL_URI = "http://www.semanticweb.org/ika/vvmethods/cruise/"
SCENARIO_PREFIX = "sce#"
CONCEPT_PREFIX = "con#"

def main():
    bs_owl = get_owl("cruise.owl")

    xlsx = pd.read_excel('criuse_reduced.xlsx')
    put_labels(xlsx, bs_owl, 'label_DE', "de")
    put_labels(xlsx, bs_owl, 'label_EN', "en")

    print(bs_owl.prettify())

    with open("cruise.owl", "w") as f:
        # f.write(bs_owl.prettify())
        f.write(str(bs_owl))



def get_owl(filename):
    with open(filename, encoding='utf-8') as owl_file:
        owl_content = owl_file.readlines()
        owl_content = "".join(owl_content)
        bs_owl = bs(owl_content, features="xml", from_encoding="utf-8")
        return bs_owl

def put_labels(t, owl, column, label):
    
    for i, row in t.iterrows():
    
        if GLOBAL_URI in row['IRI']:
            owlclass = owl.find("owl:Class", {"rdf:about" : row['IRI']})
        else:
            owlclass = owl.find("owl:Class", {"rdf:about" : GLOBAL_URI+SCENARIO_PREFIX+row['IRI']})

        if not pd.isna(row[column]):
            n = owl.new_tag('rdfs:label')
            n['xml:lang'] = label
            n.string = row[column]

            e = owlclass.find('rdfs:label', {'xml:lang': label})

            if e:
                e.replace_with(n)
                print("Overwrite  " + label + " " + row[column] + " for " + row['IRI'])
            else:
                owlclass.append(n)
                print("Put " + label + " " + row[column] + " for " + row['IRI'])
            
        else:
            print("Skipped: "+row['IRI'])


if __name__ == "__main__":
    main()
