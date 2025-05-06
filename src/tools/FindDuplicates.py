from owlready2 import get_ontology, get_namespace
import pandas as pd
import numpy as np

cruise = get_ontology('cruise.owl').load()
base_scenarios = cruise.get_namespace("http://www.semanticweb.org/ika/vvmethods/cruise/sce#")
concepts = cruise.get_namespace('http://www.semanticweb.org/ika/vvmethods/cruise/con#')
start = base_scenarios['base_scenario']

def get_children(key):
    if isinstance(key, str):
        node = cruise[key]
    else:
        node = key
    if node is None:
        return []
    else:
        return list(set([o for children in node.subclasses() for o in get_children(children)] + [node]))

def get_uppermost_concept(con):
    if np.any([o in con.is_a for o in [concepts['concept'], concepts['relative_direction']]]):
        return con
    else:
        try:
            return get_uppermost_concept(con.is_a[0])
        except KeyError:
            return con
        
bs_settings = []
base_scenarios = get_children(start)
for b in base_scenarios:
    bs_dict = {}
    bs_dict['name'] = b.name
    applies = b.INDIRECT_applies + b.applies
    for_ego = b.INDIRECT_applies_for_ego+b.applies_for_ego
    for_obj = b.INDIRECT_applies_for_obj+b.applies_for_obj
    #applies = list(set(applies) - set(for_ego) - set(for_obj))

    for values, rel in zip([applies, for_ego, for_obj],['applies','for_ego','for_obj']):
        for val in values:
            #bs_dict[f'{rel}-{get_uppermost_concept(val).iri}']=val.iri
            bs_dict[f'{rel}-{val.name}']=val.name
            #bs_dict[f'{rel}-{get_uppermost_concept(val).name}']=val.name
    bs_settings.append(bs_dict)

import pandas as pd
#keys = set([k for o in bs_settings for k in o.keys()])
df = pd.DataFrame(bs_settings)

sub_cs = [c for c in df.columns if c!='name']

duplicates = df[df.duplicated(subset=sub_cs, keep='first')]

duplicates.drop_duplicates(subset=sub_cs, keep='first', inplace=True)

# dup = duplicates[sub_cs].iloc[0]

for i, d in duplicates.iterrows():

    dup = d[sub_cs]

    # Get the concept combination
    if all(dup[sub_cs].isna()):
        print("No concepts at all\n")
    # Check if not concept at all
    else:
        print("Non-unique combination of concepts:\n")
        valid_concepts = dup[dup.notna()]
        print(valid_concepts)

    print("")
    dup_rows = df[np.logical_and(np.all([df[k]==v for k,v in dup.items() if not pd.isna(v)], axis=0), np.all(pd.isna(df[[k for k,v in dup.items() if pd.isna(v)]]),axis=1))]
    dup_rows = dup_rows[['name']+[k for k,v in dup.items() if not pd.isna(v)]]
    print(dup_rows['name'])
    print('\n'+u'\u2500' * 70+'\n')
    
