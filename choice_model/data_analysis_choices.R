# author: ptzouras

library(corrplot)
library(ggplot2)

data1<-read.csv2("datasets/choice_dataset_perceived_choices.csv", header=T,dec=".",sep=",")

corr<-function(df, x){ # plot correlation table funntion
  corel = df
  M = cor(corel)
  testRes=cor.mtest(corel, conf.level=x)
  corrplot(M, method = 'number', p.mat = testRes$p, sig.level = 1-x, diag=FALSE)} 

corr(subset(data1, select=c(binchoice1, cartime, carcost, carpsafe, young, gender)), 0.95)
corr(subset(data1, select=c(binchoice2, acttime, ebikecost, ebikepsafe, young, gender)), 0.95)
corr(subset(data1, select=c(binchoice3, acttime, escootcost, escootpsafe, young, gender)), 0.95)
