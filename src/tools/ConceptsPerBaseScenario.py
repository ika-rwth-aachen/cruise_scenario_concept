import owlready2 as owl
import json


def main():

    # Load the ontology
    cruise_path = "cruise.owl"
    crs = owl.get_ontology(cruise_path)
    crs.load()

    # Get toplevel, scenario, and concept namespaces
    cns = "http://www.semanticweb.org/ika/vvmethods/cruise"
    sce = crs.get_namespace("http://www.semanticweb.org/ika/vvmethods/cruise/sce#")
    con = crs.get_namespace("http://www.semanticweb.org/ika/vvmethods/cruise/con#")

    # Extract what we are interested in
    base_scenarios = [c for c in crs.classes() if c.namespace == sce and not list(c.subclasses())]
    superclasses = [c for c in crs.classes() if c.namespace == sce and list(c.subclasses())]
    concepts = [c for c in crs.classes() if c.namespace == con and list(c.subclasses())]
    relations = list(crs.object_properties())

    # Tuples will be displayed as lists
    print(json.dumps(get_bs_concepts(base_scenarios), sort_keys=True, indent=4))



def get_bs_concepts(base_scenarios):
    con_map={}
    for bs in base_scenarios:
        parents = bs.is_a
        cons = []
        for p in parents:
            if isinstance(p, owl.class_construct.Restriction):
                print("Got a base scenario concept. This is unexpected")
                cons.append((p.property.get_name(), p.value.get_name(p.value)))
            elif isinstance(p, owl.entity.ThingClass):
                ps_parents = p.is_a
                con = None
                for pp in ps_parents:
                    if isinstance(pp, owl.class_construct.Restriction):
                        if con:
                            print("Got two concepts for "+p.get_name(p))
                        con =(pp.property.get_name(), pp.value.get_name(pp.value))
                if con:
                    cons.append(con)
                else:
                    print("Got not concept for "+p.get_name(p))

        con_map[bs.get_name(bs)] = cons

    return con_map

 
if __name__ == "__main__":
    main()
