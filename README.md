# The PERCEIVED SAFETY CHOICES model

The model that has been uploaded to this repository aspires to describe routing behavior of micro-mobility modes, e.g., e-bikes and e-scoters, in relationship with traditional modes, e.g., private car and walking. While safety seems to be a significant factor when choosing to use these new modes, this model utilizes the notion of perceived safety to model travel behavior in inner urban areas. Therefore, the developed model is built on the hypothesis that perceived safety affects travel behavior of e-scooter users and is related to road environment.

It combines ordinal logistic regression model, which predict perceived safety in different road environments under different traffic flow conditions, with discrete choice models which give the mode choice. The input parameter is the road network which consists of links and nodes. 

Perceived safety per urban transport mode is calculated by the following equations:

<img src="https://user-images.githubusercontent.com/63541107/186910930-ed87e49d-5e63-4ff5-8dac-ff0e79bc662b.png" height="350">

Perceived safety level is integrated as an additional parameter in MATSim scoring function. This allows the use of the developed model in agent-based traffic simulations. MATSim simulates and scores many alternative travel plans (different mode or route?) in order to define an equilibrium point where agents cannot further improve their scores. Below, the new MATSim scoring function is presented (two modeling alternatives): 

<img src="https://user-images.githubusercontent.com/63541107/186910399-56406123-b7a3-499f-9599-f78390481189.png" height="150">



3. regarding the survey to estimate the unknown params

4. contents of the repository

+++ contribution to MATSim

5. paperz about the model and presentations

6. project logo: SIM4MTRAN

7. partners:

8. funded by: 
