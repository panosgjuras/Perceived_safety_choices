# Stated - rating experiment/Empirical data modeling

This package contains tools to develop empirical models that describe the impact of safety perceptions on route/mode choices. 
This empirical modeling analysis can be followed in order to calibrate the [Perceived_safety_choices](https://github.com/lotentua/Perceived_safety_choices) model considering the attitudes, the safety perceptions and in general the mobility culture existing among people in each city. 

The data are collected based on a survey form developed by Tzouras et al. ([2020](https://doi.org/10.1016/j.trip.2020.100205), [2022](https://doi.org/10.1080/15568318.2022.2037793)). The form comprises a methodological tool to take into account subjective variables related to users' perceptions in discrete choice modeling. In essence, two experiments have been combined in a single one: a) a rating experiment to measure a subjective variable (e.g., perceived safety) using 5-point of 7-point Likert Scale and a stated preferences experiment to collect route/mode choices per traffic situation. The survey design is based on a double fractional factorial design (orthogonal table); scenarios are matched in such a way that correlations among independent variables of both experiments are minimized. The survey form is given below:

<img src="https://user-images.githubusercontent.com/63541107/210239908-647afa5a-cbd2-4717-9e3f-d3696ae47619.png" height="750">

The modeling process includes an ordinal logistic regression with random variables to model users' perceptions and multinomial logit or mixed logit models to describe travel behavior based on users' perceptions. In the first modeling process, [Rchoice](https://github.com/cran/Rchoice) package is used; [PandasBiogeme](https://github.com/michelbierlaire/biogeme) is utilized for discrete choice modeling. More details and equations are given in the README files of each folder. 

The data visualization is performed in R using ggplot package [data_analysis_perceived_choices.R](https://github.com/lotentua/Perceived_safety_choices/blob/main/empirical/data_analysis_perceived_choices.R).

Multiple discrete choice models with the right settings are estimated in [BIOGEME_models_perceived_choices.py](https://github.com/lotentua/Perceived_safety_choices/blob/main/empirical/BIOGEME_models_perceived_choices.py).

Also, [logit_est_functons.py](https://github.com/lotentua/Perceived_safety_choices/blob/main/empirical/logit_est_functons.py) contains functions to directly compute an MNL or ML model using [PandasBiogeme](https://github.com/michelbierlaire/biogeme).

These tools have been developed for the PhD thesis research: "Methodologies for the integrated analysis and assessment of shared-space urban roads" conducted by [Panagiotis. G. Tzouras](https://linktr.ee/panosgtzouras) at National Technical University of Athens. The project is granted by Hellenic Foundation for Research and Innovation ([HFRI](https://www.elidek.gr/en/homepage/))
