# The PERCEIVED SAFETY CHOICES model

While safety seems to be a significant factor when choosing to use these new modes, this model utilizes the notion of perceived safety to model travel behavior in inner urban areas. Therefore, the developed model is built on the hypothesis that perceived safety affects travel behavior of micro-mobility services users and is related to road environment. It combines ordinal logistic regression model, which predict perceived safety in different road environments using a 7-point Likert Scale, with discrete choice or simulation models which simulate the mode/route choices. The input variable is the road network which consists of links and nodes. The conceptual model of the [Perceived_safety_choices](https://github.com/lotentua/Perceived_safety_choices) is presented below:

<img src="https://user-images.githubusercontent.com/121678451/210081262-8bda931f-2113-48c1-8e2c-246dc7266785.png" height="200">

The different functions of the model are parametric to take into account variations in "tastes" among individuals by proposing advance modeling techniques. All the parametric can be calibrated by collecting data related to safety perceptions considering various road environments with mixed traffic conditions and first/last mile mode/route choices in each urban area that are used. The repository contains example datasets and default models that can be used.

Based on this concept, the [Perceived_safety_choices](https://github.com/lotentua/Perceived_safety_choices) proposes some tools in order to investigate the overall impact of perceived safety on travel behavior, transport equity and transport system sustainability. There is a continuous development of these tools by the NTUA research team and external partners who still commit.

Lastly, [Perceived_safety_choices](https://github.com/lotentua/Perceived_safety_choices) creates a path to combine agent-based transport modeling (e.g., [MATSim]( https://github.com/matsim-org)) with spatial analysis and GIS tools. The new scoring function is estimated based on the Value-of-Safety (VoS) which refers to how many kilometers of less travelling a road users is willing to exchange in order to experience a better safety level. 

**The [Perceived_safety_choices](https://github.com/lotentua/Perceived_safety_choices) repository contains:**
- [Psafechoice](https://github.com/lotentua/Perceived_safety_choices/tree/main/Psafechoices): contains tools to import a shapefile with the links and nodes, estimate traffic parameters and perceived safety per link, export csv and xml files for further analysis and a routing model based on Djikstra algorithm which defines the shortest, fastest and safest path per transport mode; to do so, the [Dijkstra](https://github.com/ahojukka5/dijkstra) package is utilized; yet the weights change.
- [empirical](https://github.com/lotentua/Perceived_safety_choices/tree/main/empirical): contains advance modeling techniques based on [PandasBiogeme](https://github.com/michelbierlaire/biogeme) and [Rchoice](https://github.com/cran/Rchoice) package to compute first/last mile route/mode choice models.
- [scenario_athens](https://github.com/lotentua/Perceived_safety_choices/tree/main/scenario_athens): is an example scenario where [Psafechoice](https://github.com/lotentua/Perceived_safety_choices/tree/main/Psafechoices) functions are utilized to investigate the impact of perceived safety on route choices in the road network of the city center of Athens. Four transport modes are considered: car, e-bike, e-scooter and walk. 
- [EcarGobikes](https://github.com/lotentua/Perceived_safety_choices/tree/main/EcarGobikes): contains a multi-depot optimization model to design (flexible) first/last mile logistics service using e-bikes and inexperienced crowdshippers. The design takes into account perceived safety ratings per link.

+++ A contribution to [MATSim]( https://github.com/matsim-org) called "Psafe Module" is under development. In essence, it is an updated version of [Bicycle](https://github.com/matsim-org/matsim-libs/tree/master/contribs/bicycle) Module following a more universal approach fully based on perceived safety parameter and covering all first/last mile modes. A randomized marginal utility for the perceived safety parameter is applied in this model. The model is firstly tested using the experimental scenario in Athens.

To install the PsafeChoices package (ONLY) please type:
```bash
pip install git+https://github.com/lotentua/Perceived_safety_choices
```
Unfortunately, requirements list in the current version of the package had not fully defined! Some of them are contained in the: [requirement.txt](https://github.com/lotentua/Perceived_safety_choices/blob/main/requirements.txt)

The tools contained in this repository were developed within various research project of [LoTE](http://lte.survey.ntua.gr/main/en/).
