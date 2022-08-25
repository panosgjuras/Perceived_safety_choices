# author: ptzouras
# collaborator: valpastia

library(Rchoice)
library(corrplot)
library(ggplot2)
library(RColorBrewer)
library(ggpubr)
library(psych)

#setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
data1<-read.csv2("datasets/rating_dataset_perceived_choices.csv", header=T,dec=".",sep=",") # this is the perceived safery dataset
socio<-read.csv2("datasets/socio_dataset_perceived_choices.csv", header=T,dec=".",sep=",") # this socio-demographic dataset
# data2<-read.csv2("datasets/choice_dataset_perceived_choices.csv", header=T,dec=".",sep=",")

# 1. Descriptive statistics in sociodemo characteristics
summary(as.factor(socio$gender)) # it is balanced, male and female approx 50 - 50
summary(as.factor(socio$age)) # young young people...
# we need here a new variable...
summary(as.factor(socio$young)) # so 91 young people vs 38 over 30
# summary(as.factor(socio$income)) # income, employment and education are not factors of psafe
# summary(as.factor(socio$employment)) # so skip this variable
# summary(as.factor(socio$education))
summary(as.factor(socio$car_own)) # only 5 are not car - owners ok!!!!
summary(as.factor(socio$cycle_own)) # 72 out 129 do have a bicycle, interesting!
summary(as.factor(socio$escoot_own)) # only 8 have an e-scooter at home
summary(as.factor(socio$bike_frequency)) # very rare rare use of bicycle, even though they bicycle, 
# it cannot be used as a variable..., surely.
summary(as.factor(socio$metro_frequency)) # not useful
summary(as.factor(socio$escooter_frequency)) # we do not have e-scooter riders ok!

# 2. Descriptive statistics in psafe ratings
describe(subset(data1, tmode == 'car')$psafe)
describe(subset(data1, tmode == 'car')$psafe) # mean value equal to 5.16 - look same scenarios
describe(subset(data1, tmode == 'ebike')$psafe) # mean value equal to 3.68 - look same scenarios
describe(subset(data1, tmode == 'escoot')$psafe) # mean value equal to 3.38
describe(subset(data1, tmode == 'walk')$psafe) # mean value equal to 5.3\
# super interesting, if we order them based on safety: 1: walk, 2: car, 3: ebike and 4: escoot (the worst mode)
# compare the differences based on gender

# 3. Comparisons
# Gender
describe(subset(data1, gender == 0)$psafe)
describe(subset(data1, gender == 1)$psafe)

describe(subset(data1, tmode == 'car' & gender == 0)$psafe) # 5.03 for private car of females
describe(subset(data1, tmode == 'car' & gender == 1)$psafe) # 5.29 for private car of male, so males feel more safe to drive a car
describe(subset(data1, tmode == 'ebike' & gender == 0)$psafe) # 3.54 for ebike of females
describe(subset(data1, tmode == 'ebike' & gender == 1)$psafe) # 3.80 for ebike of male, same pattern again
describe(subset(data1, tmode == 'escoot' & gender == 0)$psafe) # 3.08 for escoot of females
describe(subset(data1, tmode == 'escoot' & gender == 1)$psafe) # 3.42 for escoot of male, same pattern again
describe(subset(data1, tmode == 'walk' & gender == 0)$psafe) # 5.30 for escoot of females
describe(subset(data1, tmode == 'walk' & gender == 1)$psafe) # 5.32 for escoot of male, no difference,
# so males feel like they are better drivers more confident etc.

# Age group
describe(subset(data1, young == 0)$psafe) # young feel safer
describe(subset(data1, young == 1)$psafe)

# lets check now the differences based on whether or they are bike owners
describe(subset(data1, tmode == 'car' & cycle_own == 0)$psafe) # 5.14, no bike owners
describe(subset(data1, tmode == 'car' & cycle_own == 1)$psafe) # 5.18 bike owners
describe(subset(data1, tmode == 'ebike' & cycle_own == 0)$psafe) # 3.56, no bike owners
describe(subset(data1, tmode == 'ebike' & cycle_own == 1)$psafe) # 3.78 bike owners
describe(subset(data1, tmode == 'escoot' & cycle_own == 0)$psafe) # 3.45, no bike owners
describe(subset(data1, tmode == 'escoot' & cycle_own == 1)$psafe) # 3.32 bike owners
describe(subset(data1, tmode == 'walk' & cycle_own == 0)$psafe) # 5.24, no bike owners
describe(subset(data1, tmode == 'walk' & cycle_own == 1)$psafe) # 5.36 bike owners

describe(subset(data1, type == 1)$psafe) # mean equal to 3.68, higher sd but this happens because of the modes.
describe(subset(data1, type == 2)$psafe) # mean equal to 4.08
describe(subset(data1, type == 3)$psafe) # mean equal to 5.4, smaller sd
describe(subset(data1, type == 4)$psafe) # mean equal to 4.38,
# let me check about shared space, what is the real impact in VRUs
describe(subset(data1, (tmode == 'walk') & (type == 4))$psafe) # smaller sd, smaller variability...
describe(subset(data1, (tmode =='escoot') & (type == 4))$psafe) 
describe(subset(data1, (tmode =='ebike') & (type == 4))$psafe)
# add shared infrastucture dummy variables to compare them with the fully segregate approach

# 4. Analysis of variance
summary(aov(data1$psafe ~ data1$gender + data1$education + data1$employment + data1$income + data1$car_own +
              data1$cycle_own + data1$bike_frequency + data1$escooter_frequency + data1$young)) # car_ownership is factor, but I have only five
summary(aov(data1$psafe ~ factor(data1$gender) + factor(data1$young) + factor(data1$tmode)))
# so psafe in general differs per mode - gender - age

# 5. Plot of main trends: sociodemo and infr. variables
hist_psafe <- function(df){ # function to plot bars, plot the responces.
  p<-ggplot(df, aes(x=as.factor(psafe), fill = tmode)) +
    geom_bar() +
    geom_text(aes(label = ..count..), stat = "count", size = 3, 
              position = position_stack(vjust = 0.5)) +
    scale_y_continuous(name ="Number of responces") +
    scale_x_discrete(name ="Perceived Safety") +
    scale_fill_brewer(palette = 'Set1', name = "Transport Mode", 
                      labels = c("Car", "E-Bike", "E-Scooter", "Walk")) + theme_bw()
  return(p)}

hist_psafe_100 <- function(df){
  p<-ggplot(df, aes(fill = factor(tmode), x = factor(psafe))) + 
    geom_bar(position = "fill") + 
    scale_fill_brewer(palette = 'Set1', name = "Transport Mode", 
                      labels = c("Car", "E-Bike", "E-Scooter", "Walk")) +
    geom_text(aes(label = scales::percent(..count../tapply(..count.., ..x.. ,sum)[..x..], accuracy = 0.1)),
              position = position_fill(vjust = 0.5),
              stat = "count") + theme_bw() +
    scale_x_discrete(name ="Perceived Safety") +
    scale_y_continuous(name ="Percentage of responces (%)", 
                       labels = function(x) paste0(x*100, "%"))
  return(p)}

# histograms: psafe vs mode vs gender (3 dimmensions of psafe) 
ggarrange(hist_psafe(subset(data1, gender == 0)) + ggtitle('Females'),
          hist_psafe(subset(data1, gender == 1)) + ggtitle('Males'),
          common.legend = TRUE, legend = 'bottom') # so here, we can see different distribution, which is super interesting
summary(aov(data1$psafe~factor(data1$gender))) # gender is definetely a factor of perceived safety in general, very high significance!!!

# histograms: psafe vs mode vs age group
ggarrange(hist_psafe_100(subset(data1, young == 1)) + ggtitle('Age < 30 years old'),
          hist_psafe_100(subset(data1, young == 0)) + ggtitle('Age >= 30 years old'),
          common.legend = TRUE, legend = 'bottom', ncol = 2) # only noticeable differences is how not young perceive safety of esooters

# histograms: psafe vs mode vs infrastructure type
ggarrange(hist_psafe(subset(data1, type==1)) + ggtitle('Type 1: Sidewalk < 1.5 m wide'),
          hist_psafe(subset(data1, type==2)) + ggtitle('Type 2: Sidewalk > 1.5 m wide'),
          hist_psafe(subset(data1, type==3)) + ggtitle('Type 3: With cycle lane'),
          hist_psafe(subset(data1, type==4)) + ggtitle('Type 4: Shared space'),
          ncol=2, nrow=2, common.legend = TRUE, legend = 'bottom') # ok this is super super, and gives clear results...in the dillemma to share or not...
# segregation is everything....they focus on the road environment, the road section...

# 6. Impact of traffic flow conditions
hist_veh_volume <- function(df){
  p<-ggplot(df, aes(fill = factor(psafe), x = factor(veh))) + 
    geom_bar(stat = "count", position = "fill") + 
    scale_fill_brewer(palette = 'RdYlBu', name = "Perceived Safety", 
                      labels = c('1: very unsafe', '2', '3', '4: moderate', '5', '6', '7: very safe')) +
    # geom_text(aes(label = scales::percent(..count../tapply(..count.., ..x.. ,sum)[..x..], accuracy = 0.1)),
    #           position = position_fill(vjust = 0.5),
    #          stat = "count") + theme_bw() +
    scale_x_discrete(name ="Vehicle density (veh/km)", labels = c('20', '60', '100')) +
    scale_y_continuous(name ="Percentage of responces (%)", 
                       labels = function(x) paste0(x*100, "%")) + coord_flip() + theme_bw()
  return(p)}

hist_bike_volume <- function(df){
  p<-ggplot(df, aes(fill = factor(psafe), x = factor(bike))) + 
    geom_bar(stat = "count", position = "fill") + 
    scale_fill_brewer(palette = 'RdYlBu', name = "Perceived Safety", 
                      labels = c('1: very unsafe', '2', '3', '4: moderate', '5', '6', '7: very safe')) +
    #geom_text(aes(label = scales::percent(..count../tapply(..count.., ..x.. ,sum)[..x..], accuracy = 0.1)),
    #          position = position_fill(vjust = 0.5),
    #          stat = "count") 
    scale_x_discrete(name ="Bike density (bikes/km)", labels = c('10', '50', '90')) +
    scale_y_continuous(name ="Percentage of responces (%)", 
                       labels = function(x) paste0(x*100, "%")) + coord_flip() + theme_bw()
  return(p)}

hist_ped_volume <- function(df){
  p<-ggplot(df, aes(fill = factor(psafe), x = factor(ped))) + 
    geom_bar(stat = "count", position = "fill") + 
    scale_fill_brewer(palette = 'RdYlBu', name = "Perceived Safety", 
                      labels = c('1: very unsafe', '2', '3', '4: moderate', '5', '6', '7: very safe')) +
    #geom_text(aes(label = scales::percent(..count../tapply(..count.., ..x.. ,sum)[..x..], accuracy = 0.1)),
    #          position = position_fill(vjust = 0.5),
    #            stat = "count") 
    scale_x_discrete(name ="Number of pedestrians (peds)", labels = c('5', '15', '25')) +
    scale_y_continuous(name ="Percentage of responces (%)", 
                       labels = function(x) paste0(x*100, "%")) + coord_flip() + theme_bw()
  return(p)}

ggarrange(hist_veh_volume(subset(data1, tmode=='car')),
          hist_bike_volume(subset(data1, tmode=='car')),
          hist_ped_volume(subset(data1, tmode=='car')),
          hist_veh_volume(subset(data1, tmode=='ebike')),
          hist_bike_volume(subset(data1, tmode=='ebike')),
          hist_ped_volume(subset(data1, tmode=='ebike')),
          hist_veh_volume(subset(data1, tmode=='escoot')),
          hist_bike_volume(subset(data1, tmode=='escoot')),
          hist_ped_volume(subset(data1, tmode=='escoot')),
          hist_veh_volume(subset(data1, tmode=='walk')),
          hist_bike_volume(subset(data1, tmode=='walk')),
          hist_ped_volume(subset(data1, tmode=='walk')), 
          nrow = 4, ncol = 3, common.legend = TRUE, legend = 'bottom') # general, general

# 7. Simple ordered logit models
data1$psafe<-as.ordered(data1$psafe)
model_car<-Rchoice(formula =  psafe ~ type1 + type2 + type4 + cross1 + cross2 + pav + obst, 
                   data = subset(data1, tmode=='car'),
                   family = ordinal("logit"), panel=FALSE, method="bfgs") # estimate ordinal logit model, select y and xs
summary(model_car) # print model results

model_ebike<-Rchoice(formula = psafe ~ type1 + type2 + type4 + cross1 + cross2 + pav + obst, 
                   data=subset(data1,tmode=='ebike'),
                   family=ordinal("logit"), panel=FALSE, method="bfgs") 
summary(model_ebike) # print model results

model_escoot<-Rchoice(formula = psafe ~ type1 + type2 + type4  + cross1 + cross2 + pav + obst, 
                   data=subset(data1,tmode=='escoot'),
                   family=ordinal("logit"), panel=FALSE, method="bfgs") 
summary(model_escoot) # print model results

model_walk<-Rchoice(formula = psafe ~ type1 + type2 + type4 + cross1 + cross2 + pav + obst, 
                   data=subset(data1, tmode=='walk'),
                   family=ordinal("logit"), panel=FALSE, method="bfgs") 
summary(model_walk) # print model results

sp_models<-data.frame(car = model_car[["coefficients"]], ebike = model_ebike[["coefficients"]],
                      escoot = model_escoot[["coefficients"]], walk = model_walk[["coefficients"]])

write.csv(sp_models,"psafe_models/outputs/simple_psafe_models.csv") # save coefficients, keep the insignificant too

# 8. TRB ordered logit models
data1$psafe<-as.ordered(data1$psafe)
model_car_TRB<-Rchoice(formula = psafe ~ gender + young + type1 + type2 + type4 + pav + cross1 + cross2 + obst + veh + bike + ped,
                      data = subset(data1, tmode=='car'),
                      ranp=c(type1="n", type2 = "n", type4 = "n", veh = "n", bike = "n", ped="n"), haltons=NA,
                      family=ordinal("logit"), index='pid',
                      panel=TRUE, R=2000, print.init = TRUE)
summary(model_car_TRB)

model_ebike_TRB<-Rchoice(formula = psafe ~ gender + young + type1 + type2 + type4 + pav + cross1 + cross2 + obst + veh + bike + ped,
                       data = subset(data1, tmode=='ebike'),
                       ranp=c(type1="n", type2 = "n", type4 = "n", veh = "n", bike = "n", ped="n"), haltons=NA,
                       family=ordinal("logit"), index='pid',
                       panel=TRUE, R=2000, print.init = TRUE)
summary(model_ebike_TRB)

model_escoot_TRB<-Rchoice(formula = psafe ~ gender + young + type1 + type2 + type4 + pav + cross1 + cross2 + obst + veh + bike + ped,
                       data = subset(data1, tmode=='escoot'),
                       ranp=c(type1="n", type2 = "n", type4 = "n", veh = "n", bike = "n", ped="n"), haltons=NA,
                       family=ordinal("logit"), index='pid',
                       panel=TRUE, R=2000, print.init = TRUE)
summary(model_escoot_TRB)

model_walk_TRB<-Rchoice(formula = psafe ~ gender + young + type1 + type2 + type4 + pav + cross1 + cross2 + obst + veh + bike + ped,
                          data = subset(data1, tmode=='walk'),
                          ranp=c(type1="n", type2 = "n", type4 = "n", veh = "n", bike = "n", ped="n"), haltons=NA,
                          family=ordinal("logit"), index='pid',
                          panel=TRUE, R=2000, print.init = TRUE)
summary(model_walk_TRB)

trb_models<-data.frame(car = model_car_TRB[["coefficients"]], ebike = model_ebike_TRB[["coefficients"]],
                      escoot = model_escoot_TRB[["coefficients"]], walk = model_walk_TRB[["coefficients"]])

write.csv(trb_models,"psafe_models/outputs/trb_psafe_models.csv") # save coefficients, keep the insignificant too

# 9. Distribution of random variables
df <- data.frame(x=1:8, y=1, col=letters[1:8])
g <- ggplot(df, aes(x=x, y=y, color=col)) + geom_point(size=5) +
  scale_color_brewer(palette="Set1")
colors <- ggplot_build(g)$data[[1]]$colour
plot(df$x, df$y, col=colors, pch=20, cex=5)

f <- function(x) (model_car_TRB[["coefficients"]][["mean.type1"]])

ggplot(data = data.frame(x = c(-12.5, 5)), aes(x)) +
  stat_function(fun = dnorm, n = 1000, args = list(mean = model_car_TRB[["coefficients"]][["mean.type1"]], 
                                                   sd = model_car_TRB[["coefficients"]][["sd.type1"]]), aes(colour = "Group 1", linetype = "Function 1"),
                size = 1.05)  +
  geom_segment(aes(x = model_car_TRB[["coefficients"]][["mean.type2"]], y = 0, xend = model_car_TRB[["coefficients"]][["mean.type2"]], yend = 1, 
                   colour = "Group 1", linetype = "Function 2"), size = 1.05) +
  geom_segment(aes(x = model_car_TRB[["coefficients"]][["mean.type4"]], y = 0, xend = model_car_TRB[["coefficients"]][["mean.type4"]], yend = 1, 
                   colour = "Group 1", linetype = "Function 3"), size = 1.05) +
  stat_function(fun = dnorm, n = 1000, args = list(mean = model_ebike_TRB[["coefficients"]][["mean.type1"]], 
                                                   sd = model_ebike_TRB[["coefficients"]][["sd.type1"]]), aes(colour = "Group 2", linetype = "Function 1"),
                size = 1.05)  +
  stat_function(fun = dnorm, n = 1000, args = list(mean = model_ebike_TRB[["coefficients"]][["mean.type2"]],
                                                   sd = model_ebike_TRB[["coefficients"]][["sd.type2"]]), aes(colour = "Group 2", linetype = "Function 2"),
                size = 1.05)  +                 
  stat_function(fun = dnorm, n = 1000, args = list(mean = model_ebike_TRB[["coefficients"]][["mean.type4"]], 
                                                   sd = model_ebike_TRB[["coefficients"]][["sd.type4"]]), aes(colour = "Group 2", linetype = "Function 3"),
                size = 1.05)  +
  stat_function(fun = dnorm, n = 1000, args = list(mean = model_escoot_TRB[["coefficients"]][["mean.type1"]], 
                                                   sd = model_escoot_TRB[["coefficients"]][["sd.type1"]]), aes(colour = "Group 3", linetype = "Function 1"),
                size = 1.05)  +
  stat_function(fun = dnorm, n = 1000, args = list(mean = model_escoot_TRB[["coefficients"]][["mean.type2"]], 
                                                   sd = model_escoot_TRB[["coefficients"]][["sd.type2"]]), aes(colour = "Group 3", linetype = "Function 2"),
                size = 1.05)  +
  stat_function(fun = dnorm, n = 1000, args = list(mean = model_escoot_TRB[["coefficients"]][["mean.type4"]], 
                                                   sd = model_escoot_TRB[["coefficients"]][["sd.type4"]]), aes(colour = "Group 3", linetype = "Function 3"),
                size = 1.05)  +
  stat_function(fun = dnorm, n = 1000, args = list(mean = model_walk_TRB[["coefficients"]][["mean.type1"]], 
                                                   sd = model_walk_TRB[["coefficients"]][["sd.type1"]]), aes(colour = "Group 4", linetype = "Function 1"),
                size = 1.05)  +
  stat_function(fun = dnorm, n = 1000, args = list(mean = model_walk_TRB[["coefficients"]][["mean.type2"]], 
                                                   sd = model_walk_TRB[["coefficients"]][["sd.type2"]]), aes(colour = "Group 4", linetype = "Function 2"),
                size = 1.05)  +
  stat_function(fun = dnorm, n = 1000, args = list(mean = model_walk_TRB[["coefficients"]][["mean.type4"]], 
                                                   sd = model_walk_TRB[["coefficients"]][["sd.type4"]]), aes(colour = "Group 4", linetype = "Function 3"),
                size = 1.05)  +
  scale_y_continuous(limits = c(0, 1.00), name = 'Probability density') + theme_bw() + scale_color_manual(values = c(colors[1],colors[2], colors[3], colors[4]),
                                                                        name = 'Transport Mode',
                                                                        labels = c("Car", "E-Bike", "E-Scooter", "Walk")) + 
  scale_linetype_manual(values = c("dashed", "dotted", "solid"), name = 'Infrastructure type',
                        labels = c("1: urban road with sidewalk < 1.5 m", "2: urban road with sidewalk >= 1.5 m", "4: shared space") ) + scale_x_continuous(name = 'Beta variable value') 

