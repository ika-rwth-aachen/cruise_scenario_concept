import owlready2 as owl

def main():

    # Load the ontology
    cruise_path = "cruise.owl"
    crs = owl.get_ontology(cruise_path)
    crs.load()

    for c in crs.classes():
        for p in c.is_a:
            if isinstance(p, owl.entity.ThingClass) \
            and not p.namespace == c.namespace:
                print(">> " + str(c) + " << does not have the same namespace as its parent >> "+ str(p) + " <<")

if __name__ == "__main__":
    main()
