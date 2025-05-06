import owlready2 as owl

cruise_path = "cruise.owl"

crs = owl.get_ontology(cruise_path)
crs.load()

cns = "http://www.semanticweb.org/ika/vvmethods/cruise"

sce = crs.get_namespace("http://www.semanticweb.org/ika/vvmethods/cruise/sce#")
con = crs.get_namespace("http://www.semanticweb.org/ika/vvmethods/cruise/con#")
attr = crs.get_namespace("http://www.semanticweb.org/ika/vvmethods/cruise/attr#")

base_scenarios = [c for c in crs.classes() if c.namespace == sce and not list(c.subclasses())]
superclasses = [c for c in crs.classes() if c.namespace == sce and list(c.subclasses())]
concepts = [c for c in crs.classes() if c.namespace == con and list(c.subclasses())]
properties = [c for c in crs.classes() if c.namespace == con and not list(c.subclasses())]
attributes = [c for c in crs.classes() if c.namespace == attr]

print(f"Number of base-scenario: {len(base_scenarios)}")
print(f"Number of superclasses: {len(superclasses)}")
print(f"Number of concepts: {len(concepts)}")
print(f"Number of properties: {len(properties)}")
print(f"Number of attributes: {len(attributes)}")