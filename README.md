# The PERCEIVED SAFETY CHOICES model

The model that has been uploaded to this repository aspires to describe routing behavior of micro-mobility modes, e.g., e-bikes and e-scoters, in relationship with traditional modes, e.g., private car and walking. While safety seems to be a significant factor when choosing to use these new modes, this model utilizes the notion of perceived safety to model travel behavior in inner urban areas. Therefore, the developed model is built on the hypothesis that perceived safety affects travel behavior of e-scooter users and is related to road environment.

It combines ordinal logistic regression model, which predict perceived safety in different road environments under different traffic flow conditions, with discrete choice models which give the mode choice. The input parameter is the road network which consists of links and nodes. 

Perceived safety per urban transport mode is calculated by the following equations:

<img src="https://user-images.githubusercontent.com/63541107/186910930-ed87e49d-5e63-4ff5-8dac-ff0e79bc662b.png" height="350">

Perceived safety level is integrated as an additional parameter in MATSim scoring function. This allows the use of the developed model in agent-based traffic simulations. MATSim simulates and scores many alternative travel plans (different mode or route?) in order to define an equilibrium point where agents cannot further improve their scores. Below, the new MATSim scoring function is presented (two modeling alternatives): 

<img src="https://user-images.githubusercontent.com/63541107/186910399-56406123-b7a3-499f-9599-f78390481189.png" height="150">

The beta parameters of the model equations have been estimated based on a survey which combines a rating experiment with a stated preferences experiment. Four different road environments are assessed in this survey, namely: type 1: urban road with sidewalk < 1.5 m wide, type 2: urban road with sidewalks ≥ 1.5 m wide, type 3: urban road with cycle lane and type 4: shared space.

<img src="https://user-images.githubusercontent.com/63541107/186911587-1eb1dbb3-eba1-492e-9cd1-d1ef76c13990.png" height="450">

The Perceived Safety Choices repository contains: 
- survey_design
- [raw_data](): collected survey data per survey block
- [psafe_models](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/psafe_models): it contains the data processing of perceived safety rating data + data analysis of perceived safety ratings in R using [Rchoice](https://github.com/cran/Rchoice) package. The output of this analysis are the beta parameters per mode + figures are included in the folder.
- [choice_models](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/choice_model): it contains data processing of choice data + model development using [Pandas BIOGEME](https://github.com/michelbierlaire/biogeme). The output of this analysis is beta parameters of choice model
- [datasets](): datasets of perceived safety ratings, sociodemographic characteristics and mode choices
- [network_analysis](): using [pyshp](https://github.com/GeospatialPython/pyshp), shps of nodes and links, in a very specific data format (see network examples), are imported to estimate perceived safety per link. The user has to provide these shp and run the code. The output of this process are xml network file capable for MATSim simualtions and csv file, which can be imported in QGIS and joined with shp for mapping purposes. 

+++ contribution to MATSim

5. paperz about the model and presentations

6. project logo: SIM4MTRAN

7. partners:

8. funded by: 
