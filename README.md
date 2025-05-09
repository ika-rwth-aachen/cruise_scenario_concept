# CRUISE

CRUISE (Comprehensive Relative Universal drIving Scenario modEl) defines a driving scenario concept.
Within the concept, traffic is categorized in base scenarios to describe the real world systematically. With its underlying ontology, the scenario concept can be understood relatively easy and different abstraction layers are included to serve different stakeholder needs.
Additionally, tools are provided to check the ontology and visualize scenarios.

> [!IMPORTANT]  
> This repository is open-sourced and maintained by the [**Institute for Automotive Engineering (ika) at RWTH Aachen University**](https://www.ika.rwth-aachen.de/).  
> **Scenario-based safety assurance** is one of many research topics within our [*Vehicle Intelligence & Automated Driving*](https://www.ika.rwth-aachen.de/en/competences/fields-of-research/vehicle-intelligence-automated-driving.html) domain.  
> If you would like to learn more about how we can support your automated driving or robotics efforts, feel free to reach out to us!  
> :email: ***opensource@ika.rwth-aachen.de***


# The ontology
[cruise.owl](cruise.owl) hosts the hierarchical structure of scenarios.
It shows which concepts are applied to derive which base-scenarios.
It gives labels for all scenarios and concepts in German and English

Generally, the ontology is subdivided into two main aspects:
- superclasses
- abstract (and refined) concepts

The concepts gives the general structure/ overview of what is specified as part of the superclasses and finally base scenarios.
The superclass branch defines the superclass-hierarchy. Leaves of this ontology are called base scenarios and are the building blocks that can be used to define scenarios.

Furthermore, a second ontology with parameters is defined, which can be used by the ase_engine.

You can view and edit the OWL file with [Protegé](https://protege.stanford.edu/).
## Supplementary material
`/res`  Holds files that were used to derive the scenario, which may however be outdated.


# Tools

## Easily manipulating labels
[src\tools\Owl2LabelXlsx.py](src\tools\Owl2LabelXlsx.py) generates a xlsx with the base scenario IDs and the related labels.
The labels can be edited in the table.
[src\tools\PutLabelsFromXlsx.py](src\tools\PutLabelsFromXlsx.py) can be used to input the labels into the ontology xml.

__Note:__ There is an issue with file encodings when doing this on Windows. This will mess up German Umlaute. Using Libre Office in Linux works well.

## Consistency checks
[src\tools\CheckNamespaces.py](src\tools\CheckNamespaces.py) can be used to check whether all entities are in the correct namespace
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
The methodology for the scenario concept is described in a peer-reviewed paper: 
[Weber, H., Glasmacher, C., Schuldes, M., Wagener, N, and Eckstein, L. "Holistic Driving Scenario Concept for Urban Traffic", 2023 IEEE Intelligent Vehicle Symposium](https://ieeexplore.ieee.org/document/10186385)

Additionally, methods and base scenarios as of 2023 are documented in a deliverable of the German research project VV Methods: 
[Glasmacher, C., Schuldes, M., Topalakatti, P., Hristov, P., Weber, H. and Eckstein, L. "Deliverable 13 - Scenario-based Model of the ODD through Scenario Databases", VVM Project, 2023](https://www.vvm-projekt.de/veroeffentlichungen)


# Acknowledgement
The initial work of this repository was done within the project “Verifikations- und Validierungsmethoden automatisierter Fahrzeuge im urbanen Umfeld” which was funded by the German Federal Ministry for Economic Affairs and Climate Action.