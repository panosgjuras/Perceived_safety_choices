# The PERCEIVED SAFETY CHOICES model

The model that has been uploaded to this repository aspires to describe routing behavior of micro-mobility modes, e.g., e-bikes and e-scoters, in relationship with traditional modes, e.g., private car and walking. While safety seems to be a significant factor when choosing to use these new modes, this model utilizes the notion of perceived safety to model travel behavior in inner urban areas. Therefore, the developed model is built on the hypothesis that perceived safety affects travel behavior of e-scooter users and is related to road environment.

It combines ordinal logistic regression model, which predict perceived safety in different road environments under different traffic flow conditions, with discrete choice models which give the mode choice. The input parameter is the road network which consists of links and nodes. 

Perceived safety per urban transport mode is calculated by the following equations:

<img src="https://user-images.githubusercontent.com/63541107/186910930-ed87e49d-5e63-4ff5-8dac-ff0e79bc662b.png" height="350">

Perceived safety level is integrated as an additional parameter in MATSim scoring function. This allows the use of the developed model in agent-based traffic simulations. MATSim simulates and scores many alternative travel plans (different mode or route?) in order to define an equilibrium point where agents cannot further improve their scores. Below, the new [MATSim](https://github.com/matsim-org) scoring function is presented (two modeling alternatives): 

<img src="https://user-images.githubusercontent.com/63541107/186910399-56406123-b7a3-499f-9599-f78390481189.png" height="150">

The beta parameters of the model equations have been estimated based on a survey which combines a rating experiment with a stated preferences experiment. Four different road environments are assessed in this survey, namely: type 1: urban road with sidewalk < 1.5 m wide, type 2: urban road with sidewalks ≥ 1.5 m wide, type 3: urban road with cycle lane and type 4: shared space.

<img src="https://user-images.githubusercontent.com/63541107/186911587-1eb1dbb3-eba1-492e-9cd1-d1ef76c13990.png" height="450">

**The Perceived Safety Choices repository contains:**
- survey_design
- [raw_data](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/raw_data): collected survey data per survey block
- [psafe_models](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/psafe_models): it contains the data processing of perceived safety rating data + data analysis of perceived safety ratings in R using [Rchoice](https://github.com/cran/Rchoice) package. The output of this analysis are the beta parameters per mode + figures are included in the folder.
- [choice_models](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/choice_model): it contains data processing of choice data + model development using [PandasBiogeme](https://github.com/michelbierlaire/biogeme). The output of this analysis is beta parameters of choice model
- [datasets](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/datasets): datasets of perceived safety ratings, sociodemographic characteristics and mode choices. These datasets can be used in other road networks (no need for new data collection).
- [network_analysis](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/network_analysis): using [pyshp](https://github.com/GeospatialPython/pyshp), shps of nodes and links, in a very specific data format (see network examples), are imported to estimate perceived safety per link. The user has to provide these shp and run the code. The output of this process are xml network file ([lxml toolkit](https://github.com/lxml/lxml) is used) capable for [MATSim](https://github.com/matsim-org) simualtions and csv file, which can be imported in GIS and joined with shp for mapping purposes.
- prediction_routing

You can run all the steps of the Perceived Safety Choices model from [Perceived_safety_choice_model.py](https://github.com/panosgjuras/Perceived_safety_choices/blob/main/Perceived_safety_choice_model.py). Analytical instructions are included there.

+++ The contribution to MATSim is under development. In essense, it is an updated version of [Bicycle](https://github.com/matsim-org/matsim-libs/tree/master/contribs/bicycle) contribution following a more universal approach fully based on perceived safety parameter and covering all micro-mobility modes.

Papers:
1. Tzouras, P. G., L. Mitropoulos, E. Stavropoulou, E. Antoniou, K. Koliou, C. Karolemeas, A. Karaloulis, K. Mitropoulos, M. Tarousi, E. I. Vlahogianni, and K. Kepaptsoglou. Agent-Based Models for Simulating e-Scooter Sharing Services: A Review and a Qualitative Assessment. International Journal of Transportation Science and Technology, 2022. https://doi.org/10.1016/j.ijtst.2022.02.001.

This model was developed for [SIM4MTRAN](http://sim4mtran.com/#/home) project that aims to develop an innovative integrated decision support tool for the design of micro-mobility systems and services. The results will be used to create a guide for the design of micro-mobility systems in urban areas in Greece supporting policy making process.

<img src="https://user-images.githubusercontent.com/63541107/186953835-3046c2e6-f965-4abf-b758-5dad32528298.png" height="200">

This research project has been co-financed by the European Regional Development Fund of the European Union and Greek national funds, National Strategic Reference Framework 2014- 2020 (NSRF), through the Operational Program Competitiveness, Entrepreneurship, and Innovation, under the call RESEARCH – CREATE – INNOVATE (project code: T2EDK-02494 and name: SIM4MTRAN).
