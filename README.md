# The PERCEIVED SAFETY CHOICES model

While safety seems to be a significant factor when choosing to use these new modes, this model utilizes the notion of perceived safety to model travel behavior in inner urban areas. Therefore, the developed model is built on the hypothesis that perceived safety affects travel behavior of micro-mobility services users and is related to road environment. It combines ordinal logistic regression model, which predict perceived safety in different road environments using a 7-point Likert Scale, with discrete choice or simulation models which simulate the mode/route choices. The input variable is the road network which consists of links and nodes. The conceptual model of the Perceived_safety_choices is presented below:

<img src="https://user-images.githubusercontent.com/121678451/210081262-8bda931f-2113-48c1-8e2c-246dc7266785.png" height="250">

The different functions of the model are parametric to take into account diffences in "tastes" among individuals by proposing advance modeling techniques. All the paremetric can be calibrated by collecting data related to safety perceptions considering various road envrironments with mixed traffic conditions and first/last mile mode/route choices in each urban area that are used. The repository contains example datasets and default models that can be used.

Based on this concept, the Perceived_safety_choices mocdel proposes some tools in order to investigate the overall impact of perceived safety on travel behavior, transport equity and transport system sustainability. There is a continuous development of these tools by the NTUA research team and external partners that commit.

Lastly, Perceived_safety_choices mocdel creates a path to combine agent-based transport modeling (like MATSim: https://github.com/matsim-org) with spatial analysis and GIS tools. The new scoring function is estimated based on the Value-of-Safety (VoS) which refers to how many kilometers of less travelling a road users is willing to exchange in order to experience a better safety level. 

**The Perceived Safety Choices repository contains:**


The model requirements are contained in the [requirement.txt](https://github.com/panosgjuras/Perceived_safety_choices/blob/main/requirements.txt) file.


**The Perceived Safety Choices repository contains:**
- survey_design: tools to design a survey, so that beta parameters of perceived safety model and routing model can be calibrated. 
- [raw_data](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/raw_data): collected survey data per survey block
- [psafe_models](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/psafe_models): it contains the data processing functions of perceived safety rating data + data analysis script of perceived safety ratings in R programming language; to run the ordingal logistic regression, the [Rchoice](https://github.com/cran/Rchoice) package is utilized.
- [choice_models](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/choice_model): it contains data processing functions of choice data + model development script using [PandasBiogeme](https://github.com/michelbierlaire/biogeme); also, funtions to estimate oppurtunity cost and marginal effects per variable are contained in this repository.
- [datasets](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/datasets): datasets of perceived safety ratings, sociodemographic characteristics and mode choices. These datasets can be used (...with the right assumptions) in other road networks; so no need for new data collection.
- [network_analysis](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/network_analysis): using [pyshp](https://github.com/GeospatialPython/pyshp), shps of nodes and links, in a very specific data format (see network examples), are imported in the developed functions to estimate perceived safety per link; the output of this process are xml network file ([lxml toolkit](https://github.com/lxml/lxml) is used) capable for [MATSim](https://github.com/matsim-org) simualtions and csv file, which can be imported in GIS and joined with shp for mapping purposes.
- [routing_model](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/routing_model): a Dijkstra routing model, which defines the shortest, fastest and safest path per transport mode; to do so, the [Dijkstra](https://github.com/ahojukka5/dijkstra) package is utilized; yet the weights change.

You can run all the steps of the Perceived Safety Choices model from [Perceived_safety_choice_model.py](https://github.com/panosgjuras/Perceived_safety_choices/blob/main/Perceived_safety_choice_model.py). Analytical instructions are included there (with comments). 

+++ The contribution to MATSim is under development. In essense, it is an updated version of [Bicycle](https://github.com/matsim-org/matsim-libs/tree/master/contribs/bicycle) contribution following a more universal approach fully based on perceived safety parameter and covering all micro-mobility modes.

Papers:
1. Tzouras, P. G., L. Mitropoulos, E. Stavropoulou, E. Antoniou, K. Koliou, C. Karolemeas, A. Karaloulis, K. Mitropoulos, M. Tarousi, E. I. Vlahogianni, and K. Kepaptsoglou. Agent-Based Models for Simulating e-Scooter Sharing Services: A Review and a Qualitative Assessment. International Journal of Transportation Science and Technology, 2022. https://doi.org/10.1016/j.ijtst.2022.02.001.

