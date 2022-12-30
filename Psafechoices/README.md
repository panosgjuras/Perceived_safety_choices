The [Psafechoices](https://github.com/lotentua/Perceived_safety_choices/edit/main/Psafechoices) tools contained in this folder were developed for [SIM4MTRAN](http://sim4mtran.com/#/home) project that aims to develop an innovative integrated decision support tool for the design of micro-mobility systems and services. The results will be used to create a guide for the design of micro-mobility systems in urban areas in Greece supporting policy making process.

The routing model is based on the following equation:

<img src="https://user-images.githubusercontent.com/121678451/210090788-3fa9a89f-1ad3-4bdf-80f6-cf42dfd45576.png" width="600">

**The [Psafechoices](https://github.com/lotentua/Psafechoices) contains:**

-[psafe_coeff_upd.py](https://github.com/lotentua/Perceived_safety_choices/blob/main/Psafechoices/psafe_model/psafe_coeff_upd.py): updates the kappa threshold exported from [Rchoice](https://github.com/cran/Rchoice) package that introduces an intercept in the ordered logit model. The intercept do not influence the latent variable in practice; it is related to the kappa thresholds;           

-[opp_cost_calculator.py](https://github.com/lotentua/Perceived_safety_choices/blob/main/Psafechoices/choice_model/opp_cost_calculator.py): estimates from a route/mode choice model the marginal utilities to be impoted in [MATSim]( https://github.com/matsim-org) scoring function and the Value-of-Safety expressed in meters/level; THESE FUNCTIONS ARE STILL UNDER DEVELOPMENT in order to integrate Monte-Carlo Simulation in the estimation of VoS;

-[network_analysis](https://github.com/lotentua/Perceived_safety_choices/tree/main/Psafechoices/network_analysis) functions: using [pyshp](https://github.com/GeospatialPython/pyshp), shps of nodes and links, in a very specific data format (see network examples), are imported in the developed functions to estimate perceived safety per link; the output of this process are xml network file ([lxml toolkit](https://github.com/lxml/lxml) is used) capable for [MATSim](https://github.com/matsim-org) simualtions and csv file, which can be imported in GIS and joined with shp for mapping purposes.

-[routing_model](https://github.com/panosgjuras/Perceived_safety_choices/tree/main/routing_model): a Dijkstra routing model, which defines the shortest, fastest and safest path per transport mode; to do so, the [Dijkstra](https://github.com/ahojukka5/dijkstra) package is utilized; yet the weights change. Critical parameters are: a) the maximum acceptable unsafe distance (dmax) after which perceived safety significantly increases (or decreases) the utility of traveling from the link i and b) the minimum acceptable perceived safety level (minv) is related to the confidence of one road user to use the transport mode m in less safe links i. These parameters should be calibrated. STOCHASTIC MODEL WILL BE INTEGRATED TOO.

<img src="https://user-images.githubusercontent.com/63541107/186953835-3046c2e6-f965-4abf-b758-5dad32528298.png" height="150">

This research project has been co-financed by the European Regional Development Fund of the European Union and Greek national funds, National Strategic Reference Framework 2014- 2020 (NSRF), through the Operational Program Competitiveness, Entrepreneurship, and Innovation, under the call RESEARCH – CREATE – INNOVATE (project code: T2EDK-02494 and name: SIM4MTRAN).
