library(ggplot2)
library(reshape2)
library(ggpubr)
library(psych)

color <- data.frame(car = "#C4322A", ebike = "#F2B16E", 
                    escoot = "#B5D8E7", walk = "#4379B1")

readf <- function(scenario, typ, t){
  setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
  if(typ =="pkm"){add = "pkm_modestats.txt"}
  if(typ == "ph"){add = "ph_modestats.txt"}
  if(typ == "mode"){add = "modestats.txt"}
  path <- paste("aggregate_all_test_scenarios/",scenario,add, sep = "/")
  pkm <- read.table(path, header = T)
  pkm$total <- pkm$car + pkm$ebike + pkm$escoot
  pkm$perc_car <- pkm$car/pkm$total
  pkm$perc_ebike <- pkm$ebike/pkm$total
  pkm$perc_escoot <- pkm$escoot/pkm$total
  pkm$scenario <- paste(t,scenario, sep = ": ")
  return(pkm)}

meltT <- function(indf, typ = 'total'){
  if(typ == 'total'){
  df <- melt(indf, id.vars=c('Iteration', 'scenario'),
             measure.vars=c('car', 'ebike', 'escoot'))}
  if(typ == 'perc'){
    df <- melt(indf, id.vars=c('Iteration', 'scenario'),
               measure.vars=c('perc_car', 'perc_ebike', 'perc_escoot'))}
  return(df)}

anabox <- function(df){
  ggplot(subset(meltT(df, 'perc'), !(variable %in% c('perc_car'))), aes(x = as.factor(variable), y = value)) +
    geom_boxplot(aes(fill = variable)) + theme_bw() +
    geom_point(size = 1.5, alpha = .3, position = position_jitter(seed = 1, width = .2)) +
    scale_fill_manual(values = c(color$ebike, color$escoot), labels = c("e-bike", "e-scooter")) +
    scale_y_continuous(name = "Share of passenger kilometers", limits = c(0.0, 0.35)) +
    scale_x_discrete(name = "Transport Mode", labels = c("e-bike", "e-scooter"))}

analine <- function(df, scenarios, limit = c(0, 5500)){
  vars = c('car')
  ggplot(subset(meltT(df), !(variable %in% vars))) +
    geom_line(aes(x = Iteration, y = value, color = variable, linetype = scenario)) +
    theme_bw() + scale_x_continuous(limits = c(0,100)) +
    scale_y_continuous(name = "Total passenger kilometers", limits = limit) +
    scale_linetype_manual(name = "Scenario", 
                          values = c("solid", "dashed", "dotted", "dotdash"), 
                          labels = scenarios) + 
    scale_color_manual(values = c("red", "blue"), labels = c("e-bike", "e-scooter"))
  }

newanaline<-function(df1, df2, set = "set1", mode = "Car", mm = 3.0, mx = 8.0){
  if(mode == 'Car'){vars = c('ebike', 'escooter')}
  if(mode == 'E-bike'){vars = c('car', 'escooter')}
  if(mode == 'E-scooter'){vars = c('car', 'ebike')}
  
  if(set == 'set1'){
    scenarios = c("Weighted average", "Dmax = 500 m", 
                 "Dmax = 1500 m", "Dmax = 3000 m")
    pal = c("#4c0000", "#b3002a","#ff0000", "#ffb3c5")}
  if(set == 'set2'){
    scenarios = c("Rm = 15%; Rr = 5%",  "Rm = 10%; Rm = 10%", "Rm = 5%; Rr = 15%")
    pal = c("#520066", "#cc00ff", "#eb99ff")}
  if(set == 'set3'){
    scenarios = c("Scenario 000", "Scenario 000 with Psafe module",
                   "Scenario 000 with Psafe module and sd")
    pal = c("#003180", "#0061ff", "#b3d0ff")}
  if(set == 'set4'){
    scenarios = c("Scenario 100", "Scenario 100 with Psafe module",
                   "Scenario 100 with Psafe module and sd")
    pal = c("#00660a", "#00ff1a", "#b3ffba")}

  ndf <- merge(df1, df2, by = c("Iteration", "scenario"))
  
  fdf <- data.frame(Iteration = ndf$Iteration, 
                    scenario = ndf$scenario,
                    car = ndf$car.y/ndf$car.x,
                    ebike = ndf$ebike.y/ndf$ebike.x,
                    escoot = ndf$escoot.y/ndf$escoot.x)
  
  fdf <- subset(meltT(fdf), !(variable %in% vars))
  print(fdf)
  
  ggplot(fdf) + geom_line(aes(x = Iteration, y = value, color = scenario)) +
    theme_bw() + scale_y_continuous(name = 'Average trip distance in km', 
                                    limits = c(mm, mx)) +
    scale_color_manual(name = "", values = pal, labels = scenarios) + ggtitle(mode)
  }

descrfun <- function(df, scen, iter = 100, x = 1000){
  print(describe(subset(df, df$scenario == scen)$car)/x)
  print(subset(df, (df$scenario == scen) & (df$Iteration == iter))$car/x)
  
  print(describe(subset(df, df$scen == scen)$ebike)/x)
  print(subset(df, (df$scenario == scen) & (df$Iteration == iter))$ebike/x)
  
  print(describe(subset(df, df$scen == scen)$escoot)/x)
  print(subset(df, (df$scenario == scen) & (df$Iteration == iter))$escoot/x)}

#################################
# from 9000 to 5000 and vice versa
pm1 <- readf("scenario_dmax0", "mode", 0)
pm1 <- rbind(pm1, readf("scenario_dmax500", "mode", 1))
pm1 <- rbind(pm1, readf("scenario_dmax1500", "mode", 2))
pm1 <- rbind(pm1, readf("scenario_dmax3000", "mode", 3))
pm1$car <- as.integer(pm1$car * 2400)
pm1$ebike <- as.integer(pm1$ebike * 2400)
pm1$escoot <- as.integer(pm1$escoot * 2400)
descrfun(pm1, "0: scenario_dmax0",)
descrfun(pm1, "1: scenario_dmax500")
descrfun(pm1, "2: scenario_dmax1500")
descrfun(pm1, "3: scenario_dmax3000")

pkm1 <- readf("scenario_dmax0", "pkm", 0)
pkm1 <- rbind(pkm1, readf("scenario_dmax500", "pkm", 1))
pkm1 <- rbind(pkm1, readf("scenario_dmax1500", "pkm", 2))
pkm1 <- rbind(pkm1, readf("scenario_dmax3000", "pkm", 3))
descrfun(pkm1, "0: scenario_dmax0")
descrfun(pkm1, "1: scenario_dmax500")
descrfun(pkm1, "2: scenario_dmax1500")
descrfun(pkm1, "3: scenario_dmax3000")

p1 <- newanaline(pm1, pkm1, "set1", "Car", 5.5, 7.5)
p2 <- newanaline(pm1, pkm1, "set1", "E-bike", 5.5, 7.5)
p3 <- newanaline(pm1, pkm1, "set1", "E-scooter", 5.5, 7.5)
p100<- ggarrange(p1, p2, p3, ncol = 3, nrow = 1, common.legend = TRUE, 
          legend = "bottom" )
p100
###################################



###################################
# from 9000 to 5000 and vice versa
pm2 <- readf("scenario_replan100", "mode", 2)
pm2 <- rbind(pm2, readf("scenario_replan101", "mode", 1))
pm2 <- rbind(pm2, readf("scenario_replan102", "mode", 0))
pm2$car <- as.integer(pm2$car * 2400)
pm2$ebike <- as.integer(pm2$ebike * 2400)
pm2$escoot <- as.integer(pm2$escoot * 2400)
descrfun(pm2, "2: scenario_replan100")
descrfun(pm2, "1: scenario_replan101")
descrfun(pm2, "0: scenario_replan102")

pkm2 <- readf("scenario_replan100", "pkm", 2)
pkm2 <- rbind(pkm2, readf("scenario_replan101", "pkm", 1))
pkm2 <- rbind(pkm2, readf("scenario_replan102", "pkm", 0))
descrfun(pkm2, "2: scenario_replan100")
descrfun(pkm2, "1: scenario_replan101")
descrfun(pkm2, "0: scenario_replan102")

p4 <- newanaline(pm2, pkm2, "set2", "Car", 5.5, 7.5)
p5 <- newanaline(pm2, pkm2, "set2", "E-bike", 5.5, 7.5)
p6 <- newanaline(pm2, pkm2, "set2", "E-scooter", 5.5, 7.5)
p200<- ggarrange(p4, p5, p6, ncol = 3, nrow = 1, common.legend = TRUE, 
                 legend = "bottom" )
p200
###################################

###################################
# from 9000 to 5000 and vice versa
pm3 <- readf("scenario000", "mode", 0)
pm3 <- rbind(pm3, readf("scenario000_psafemodule", "mode", 1))
pm3 <- rbind(pm3, readf("scenario000_psafemodule_sd", "mode", 2))
pm3$car <- as.integer(pm3$car * 2400)
pm3$ebike <- as.integer(pm3$ebike * 2400)
pm3$escoot <- as.integer(pm3$escoot * 2400)
descrfun(pm3, "0: scenario000")
descrfun(pm3, "1: scenario000_psafemodule")
descrfun(pm3, "2: scenario000_psafemodule_sd")

pkm3 <- readf("scenario000", "pkm", 0)
pkm3 <- rbind(pkm3, readf("scenario000_psafemodule", "pkm", 1))
pkm3 <- rbind(pkm3, readf("scenario000_psafemodule_sd", "pkm", 2))
descrfun(pkm3, "0: scenario000")
descrfun(pkm3, "1: scenario000_psafemodule")
descrfun(pkm3, "2: scenario000_psafemodule_sd")
p7 <- newanaline(pm3, pkm3, "set3", "Car", 4.00, 6.0)
p8 <- newanaline(pm3, pkm3, "set3", "E-bike", 4.0, 6.0)
p9 <- newanaline(pm3, pkm3, "set3", "E-scooter", 4.0, 6.0)
p300<- ggarrange(p7, p8, p9, ncol = 3, nrow = 1, common.legend = TRUE, 
                 legend = "bottom" )
p300
###################################

###################################
# from 9000 to 5000 and vice versa
pm4 <- readf("scenario100", "mode", 0)
pm4 <- rbind(pm4, readf("scenario100_psafemodule", "mode", 1))
pm4 <- rbind(pm4, readf("scenario100_psafemodule_sd", "mode", 2))
pm4$car <- as.integer(pm4$car * 2400)
pm4$ebike <- as.integer(pm4$ebike * 2400)
pm4$escoot <- as.integer(pm4$escoot * 2400)
descrfun(pm4, "0: scenario100")
descrfun(pm4, "1: scenario100_psafemodule")
descrfun(pm4, "2: scenario100_psafemodule_sd")

pkm4 <- readf("scenario100", "pkm", 0)
pkm4 <- rbind(pkm4, readf("scenario100_psafemodule", "pkm", 1))
pkm4 <- rbind(pkm4, readf("scenario100_psafemodule_sd", "pkm", 2))

descrfun(pkm4, "0: scenario100")
descrfun(pkm4, "1: scenario100_psafemodule")
descrfun(pkm4, "2: scenario100_psafemodule_sd")
p10 <- newanaline(pm4, pkm4, "set4", "Car", 4.00, 6.0)
p11 <- newanaline(pm4, pkm4, "set4", "E-bike", 4.0, 6.0)
p12 <- newanaline(pm4, pkm4, "set4", "E-scooter", 4.0, 6.0)
p400<- ggarrange(p10, p11, p12, ncol = 3, nrow = 1, common.legend = TRUE, 
                 legend = "bottom" )
p400
###################################

ggarrange(p100, p200, ncol = 1, nrow = 2)
ggarrange(p300, p400, ncol = 1, nrow = 2)

