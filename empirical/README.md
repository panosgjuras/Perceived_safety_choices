# Image based double stated preferences experiment - Empirical modeling

This package contains tools to develop empirical models that describe the impact of safety perceptions on route/mode choices. 
This empirical modeling analysis can be followed in order to calibrate the [Perceived_safety_choices](https://github.com/lotentua/Perceived_safety_choices) model considering the attitudes, the safety perceptions and in general the mobility culture existing among people in each city. 

The modeling process includes an ordinal logistic regression with random variables to model users' perceptions and multinomial logit or mixed logit models to describe travel behavior based on users' perceptions. In the first modeling process, [Rchoice](https://github.com/cran/Rchoice) package is used; [PandasBiogeme](https://github.com/michelbierlaire/biogeme) is utilized for discrete choice modeling. The model equations are summarized below: 

$psafe_{l,j,m}^{*} + ε_{l,j,m} = ∑_{i=1}^{4} β_{soc_{i,m}}*soc_{i,j} + ∑_{i=1}^{5} β_{beh_{i,m}}*beh_{i,j} + ( β_{infr_{1,m}} * infr_{1,l} + β_{infr_{2,m}} * infr_{2,l} + β_{infr_{3,m}} * infr_{3,l} + $
$β_{pav_{m}}*pav_{l} + β_{obs_{m}} * obs_{l} + β_{crs_{1,m}} * crs_{1,l} + β_{crs_{2,m}} * crs_{2,l}) +$
$(β_{veh_{m}} * veh_{l} + β_{bike_{m}} * bike_{l} + β_{ped_{m}} *ped_{l})  + ε_{l,j,m}$

$psafe_{j,l,m} = 1$, if $psafe_{l,j,m}^{*} ≤ k_{1,m}$, very unsafe

$psafe_{j,l,m} = 2$, if $k_{1,m} ≤ psafe_{l,j,m}^{*} ≤ k_{2,m}$

$psafe_{j,l,m} = 3$, if $k_{2,m} ≤ psafe_{l,j,m}^{*} ≤ k_{3,m}$

$psafe_{j,l,m} = 4$, if $k_{3,m} ≤ psafe_{l,j,m}^{*} ≤ k_{4,m}$

$psafe_{j,l,m} = 5$, if $k_{4,m} ≤ psafe_{l,j,m}^{*} ≤ k_{5,m}$

$psafe_{j,l,m} = 6$, if $k_{5,m} ≤ psafe_{l,j,m}^{*} ≤ k_{6,m}$

$psafe_{j,l,m} = 7$, if $k_{6,m} < psafe_{l,j,m}^{*}$, very safe

where:
$psafe_{l,j,m}^{*}$: latent variable of perceived safety of individual j using mode m in urban road link l (or observation l);
$psafe_{j,l,m}$: perceived safety level of individual j using mode m in urban road link l (or observation l);
$β_{infr_{1,m}}, β_{infr_{2,m}}, ...,β_{ped,m}$: beta parameters of latent perceived safety function of mode m;
$k_{1,m}, k_{2,m}, ...,k_{6,m}$: perceived safety kappa thresholds of mode m;
$ε_{l,j,m}$: error term
$soc_{i,j}$: sociodemographic characteristics of individual j;
$beh_{i,j}$: travel behavior attributes of individual j;

$β_{infr_{1,m}}$: 1, if there is an urban road with sidewalks less than 1.5 m wide and without cycle lane in urban road link l – type 1;
$β_{infr_{2,m}}$: 1, if there is an urban road with sidewalks equal to or more than 1.5 m wide and without cycle lane in urban road link l – type 2;
$β_{infr_{3,m}}$: 1, if shared space in urban road link l – type 3 (all infr parameters equal to 0, if there is an urban road with sidewalks equal to or more than 1.5 m wide and with cycle lane – type 0);
$pav_{i}$: 1, if the pavement of the urban road is in a good condition urban road link l;
$obs_{i}$: 1, if there are obstacles in the road environment urban road link l;
$crs_{1,l}$: 1, if there is an unsignalized zebra pedestrian crossing in the next 200 meters of urban road link l;
$crs_{2,l}$: 1, if there is a signalized zebra pedestrian crossing in the next 200 meters of urban road link l (all crs parameters equal to 0, if there is no zebra pedestrian crossing in the next 200 meters);

$veh_{l}$: car density in vehicles per km per direction of urban road link i;
$bike_{l}$: bike density in bikes per km per direction of urban road link i;
$ped_{l}$: number of pedestrians in the road environment (next 50 m) of urban road link i.

$U_{r,j,\ m}=\ V_{r,j,\ m}+\varepsilon_{r,j,\ m}=ASC_m+\beta_{time_m}\ast time_{m,\ r}+\beta_{cost_m}\ast cost_{m,r}+\beta_{psafe_m}\ast\left(\ psafe_{j,r,\ \ m}-4\right)+\varepsilon_{j,r,m}\ \ \$

where:
$U_{j,\ r,\ m}$: utility of using mode m in first/last mile route r by individual j;
$V_{r,j,\ m}$: systematic utility of using mode m in first/last mile route r by individual j;
$\beta_{time_m},\ \beta_{cost_m},\beta_{psafe_m}$: beta parameters of utility function of mode m;
$\varepsilon_{j,l,m}$: error term;
$ASC_m$: alternative specific constant of mode m; 
$time_{m,\ r}$: travel time of using mode m in first/last mile route r;
$cost_{m,r}$: travel cost of using mode m in first/last mile route r;
$psafe_{j,l,\ \ m}$: perceived safety level of mode m in first/last mile route r, as it is experienced by individual r.

The data are collected based on a survey form developed by [Tzouras et al. (2020](https://doi.org/10.1016/j.trip.2020.100205), [2022)](https://doi.org/10.1080/15568318.2022.2037793). The form comprises a methodological tool to take into account subjective variables related to users' perceptions in discrete choice modeling. In essence, two experiments have been combined in a single one: a) a rating experiment to measure a subjective variable (e.g., perceived safety) using 5-point of 7-point Likert Scale and a stated preferences experiment to collect route/mode choices per traffic situation. The survey design is based on a double fractional factorial design (orthogonal table); scenarios are matched in such a way that correlations among independent variables of both experiments are minimized. The survey form is given below:

<img src="https://user-images.githubusercontent.com/63541107/210239908-647afa5a-cbd2-4717-9e3f-d3696ae47619.png" height="750">

The data visualization is performed in R using ggplot package [data_analysis_perceived_choices.R](https://github.com/lotentua/Perceived_safety_choices/blob/main/empirical/data_analysis_perceived_choices.R).

Multiple discrete choice models with the right settings are estimated in [BIOGEME_models_perceived_choices.py](https://github.com/lotentua/Perceived_safety_choices/blob/main/empirical/BIOGEME_models_perceived_choices.py).

Also, [logit_est_functons.py](https://github.com/lotentua/Perceived_safety_choices/blob/main/empirical/logit_est_functons.py) contains functions to directly compute an MNL or ML model using [PandasBiogeme](https://github.com/michelbierlaire/biogeme).

The advantage of this approach is that it models the heterogeneity of safety perceptions among individuals. Additionaly, it also considers that the impact of safety perceptions in choices can also be randomized. It differs per individual. Therefore, it connects road environment with safety perceptions, and safety perceptions with mobility choices through stochasticity.
