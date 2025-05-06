# CRUISE

CRUISE (Comprehensive Relative Universal drIving Scenario modEl) defines a driving scenario concept.
Within the concept, traffic is categorized in base scenarios to descripe the real-world systematically. With its underlying ontology, the scenario concept can be understood relatively easy and different abstraction layers are included to sever different stakeholder needs. 
Additionally, tools are provided to check the ontology and visualize scenarios.

# The ontology
[cruise.owl](cruise.owl) hosts the hierarchical structure of scenarios.
It shows which concepts are applied to derive which base-scenarios.
It gives labels for all scenarios and concepts in German and English

Generally, the ontology is subdivided into two main aspects:
- superclasses
- abstract (and refined) concepts

The concepts gives the general structure/ overview over what is specified as part of the superclasses and finally base scenarios.
The superclass branch defines the superclass-hierachy. Leaves of this ontology are called base scenarios and are the building blocks which can be used to define scenarios.

Furthermore, a second ontology with parameters is defined which can be used by the ase_engine.

You can view and edit the OWL file with [Protegé](https://protege.stanford.edu/).
## Supplementary material
`/res`  Holds files that were used to derive the scenario, which may however be outdated.

# Tools

## Easily manipulating labels
[src\tools\Owl2LabelXlsx.py](src\tools\Owl2LabelXlsx.py) generates an xlsx with the base scenario IDs and the related labels.
The labels can be edited in the table.
[src\tools\PutLabelsFromXlsx.py](src\tools\PutLabelsFromXlsx.py) can be used to input the labels into the ontology xml.

__Note:__ There is an issue with file encodings, when doing this on Windows. This will mess up German Umlaute. Using Libre Office in Linux works well.

## Consitensy checks
[src\tools\CheckNamespaces.py](src\tools\CheckNamespaces.py) can be used to check, whether all entities are in the correct namespace
- scenario -> `sce`
- concepts -> `con`
- attribute -> `attr`

[src\tools\FindDuplicates.py](src\tools\FindDuplicates.py) can be used to verify that each base-scenario is derived from a unique combination of concepts.

[src\tools\CountEntities.py](src\tools\CountEntities.py) gets the number of base-scenario and concepts.

# Output:
[src\draw\DrawFromOwl.py](src\draw\DrawFromOwl.py) generates the images for all base scenarios which are used in the .md and .html tables.

[src\tools\PublishAsTable.py](src\tools\PublishAsTable.py)
The scenarios can be published in tablular formats, as xlsx, .md and .html.
(.xlsx will be without images.)

# References
The methodology for the scenario concept is described in a peer-reviewed paper: [Paper](https://ieeexplore.ieee.org/document/10186385)
Additionally, methods and base scenarios as of 2023 are documented in a deliverable of the German research project VV Methods: [Deliverable-13](https://www.vvm-projekt.de/securedl/sdl-eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NDYxMzQ1NjcsImV4cCI6MTc0NjIyNDU2NywidXNlciI6MCwiZ3JvdXBzIjpbMCwtMV0sImZpbGUiOiJmaWxlYWRtaW4vdXNlcl91cGxvYWQvUGFwZXJzL0RlbGl2ZXJhYmxlMTMtU2NlbmFyaW8tYmFzZWRfTW9kZWxfb2ZfdGhlX09ERF90aHJvdWdoX1NjZW5hcmlvX0RhdGFiYXNlcy5wZGYiLCJwYWdlIjoyM30.VrPMuoxYUvAoccG1FtkFoKf87SvafqrlVSs18Eg0Nas/Deliverable13-Scenario-based_Model_of_the_ODD_through_Scenario_Databases.pdf)