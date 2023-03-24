# The "Scenario Athens"

It is an experimental scenario developed in the Athens, Greece downtown area. The scenario is useful for testing first/last mile transport systems, e.g., e-bikes, e-scooters, etc. Most of the trip distances do not exceed the 10 km. The study area includes Athens’ commercial triangle where shops, hotels, restaurants, etc. are concentrated. In addition, Ministries and Public Services can be found around Syntagma Square and Panepistimiou Avenue. The road network mostly consists of narrow (one way) streets and pedestrianized zones, which hinder the use of private cars. As an alternative, there are six metro sta-tions and two tram stations, which support the trips from/to the city center of Athens making public transport as the most efficient and therefore attractive option for accessing to the study area. 

The road network consist of 257 nodes and 400 links!

It is an example scenario for potential users of [Psafechoices](https://github.com/lotentua/Perceived_safety_choices/tree/main/Psafechoices) package

Pedestrianized streets have been excluded. Some exceptions to this are Aiolou Street and the route from Dion. Aeropagitou and Apost. Pavlou Streets, which comprise a wide, 1.38 km long pedestrianized route that connects the Acropolis of Athens with the Ancient Market. In the developed network, there are no cycle lanes with the exemption of Vas. Olgas and Panepistimiou Avenues where pop-up cycle lanes were established in May 2020.

For simplicity, only nine external zones are specified, i.e., node 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000 and 9000. These zones are connected with the established road network via a single uni-directional link. 

The spatial data that describe road infrastructure have been collected in a standarized format. In the [shapefile](https://github.com/lotentua/Perceived_safety_choices/tree/main/scenario_athens/shapefiles) folder, there are .qml files  with the respective styles. In QGIS, spatial data are imported using a dropdown menu. Please follow these styles, otherwise the [Psafechoices](https://github.com/lotentua/Perceived_safety_choices/tree/main/Psafechoices) package cannot be used to process the spatial data. Attention, use the SNAPPING tool in QGIS, so that the start/end point of a link will have the same coordinates with the respective node.

This the first scenario in Athens Metropolitan Area developed for Agent-Based Simulations and First/Last Mile Routing. More updates are coming in the future.

<img width="700" alt="image" src="https://user-images.githubusercontent.com/121678451/227531934-ae135d3b-f5d5-4614-8379-07be2ff51cc4.png">
