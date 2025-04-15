# The PERCEIVED SAFETY CHOICES model

While safety seems to be a significant factor when choosing to use these new modes, this model utilizes the notion of perceived safety to model travel behavior in inner urban areas. Therefore, the developed model is built on the hypothesis that perceived safety affects travel behavior of micro-mobility services users and is related to road environment. It combines ordinal logistic regression model, which predict perceived safety in different road environments using a 7-point Likert Scale, with discrete choice or simulation models which simulate the mode/route choices. The input variable is the road network which consists of links and nodes. The conceptual model of the [Perceived_safety_choices](https://github.com/lotentua/Perceived_safety_choices) is presented below:

<img src="https://user-images.githubusercontent.com/121678451/210081262-8bda931f-2113-48c1-8e2c-246dc7266785.png" height="200">

The different functions of the model are parametric to take into account variations in "tastes" among individuals by proposing advance modeling techniques. All the parametric can be calibrated by collecting data related to safety perceptions considering various road environments with mixed traffic conditions and first/last mile mode/route choices in each urban area that are used. The repository contains example datasets and default models that can be used.

Based on this concept, the [Perceived_safety_choices](https://github.com/lotentua/Perceived_safety_choices) proposes some tools in order to investigate the overall impact of perceived safety on travel behavior, transport equity and transport system sustainability. There is a continuous development of these tools by the NTUA research team and external partners who still commit.

Lastly, [Perceived_safety_choices](https://github.com/lotentua/Perceived_safety_choices) creates a path to combine agent-based transport modeling (e.g., [MATSim]( https://github.com/matsim-org)) with spatial analysis and GIS tools. 

**The [Perceived_safety_choices](https://github.com/panogjuras/Perceived_safety_choices) repository contains:**
- [Psafechoice](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/Psafechoices): contains tools to import a shapefile with the links and nodes, estimate traffic parameters and perceived safety per link, export csv and xml files for further analysis and a routing model based on Value-of-Safety and new algorithms that define the shortest, fastest and safest path per transport mode.
- [empirical](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/empirical): contains advance modeling techniques based on [PandasBiogeme](https://github.com/michelbierlaire/biogeme) and [Rchoice](https://github.com/cran/Rchoice) package to compute first/last mile route/mode choice models.

The jupyter notebook of [scenario_athens](https://github.com/panosgjuras/Perceived_safety_choices/blob/main/scenario_Athens.ipynb) gives analytical guidelines how some of the developed functions can be used. It considers an example scenario developed in Athens, Greece.

Lastly, [Perceived_safety_choices](https://github.com/lotentua/Perceived_safety_choices) creates a path to combine agent-based transport modeling and [MATSim]( https://github.com/matsim-org) with spatial analysis and GIS tools. The contribution in MATSim framework have been developed and can be found: [Psafe module](https://github.com/panosgjuras/Psafe). In essence, it is an updated version of [Bicycle](https://github.com/matsim-org/matsim-libs/tree/master/contribs/bicycle) Module following a more universal approach fully based on perceived safety parameter and covering all first/last mile modes. A randomized marginal utility for the perceived safety parameter is applied in this model. The model is firstly tested using the experimental scenario in Athens.

To install the PsafeChoices package (ONLY) please type:
```bash
pip install git+https://github.com/panosgjuras/Perceived_safety_choices
```
Requirements are contained in the: [requirement.txt](https://github.com/lotentua/Perceived_safety_choices/blob/main/requirements.txt)

The research findings obtained using the tools in this package are documented in the following published papers:
> Tzouras, P.G., Mitropoulos, L., Karolemeas, C., Stravropoulou, E., Vlahogianni, E.I., Kepaptsoglou, K., 2024. Agent-based simulation model of micro-mobility trips in heterogeneous and perceived unsafe road environments. Journal of Cycling and Micromobility Research 2, 100042. [https://doi.org/10.1016/j.jcmr.2024.100042]

> Tzouras, P.G., Pastia, V., Kaparias, I., Kepaptsoglou, K., 2024. Exploring the effect of perceived safety in first/last mile mode choices. Transportation. [https://doi.org/10.1007/s11116-024-10487-4]

> Tzouras, P.G., Mitropoulos, L., Koliou, K., Stavropoulou, E., Karolemeas, C., Antoniou, E., Karaloulis, A., Mitropoulos, K., Vlahogianni, E.I., Kepaptsoglou, K., 2023. Describing Micro-Mobility First/Last-Mile Routing Behavior in Urban Road Networks through a Novel Modeling Approach. Sustainability 15, 3095. [https://doi.org/10.3390/su15043095]


