# author: ptzouras

library(corrplot)
library(ggplot2)
library(ggpubr)
library(psych)
library(RColorBrewer)
library(scales)  

data1<-read.csv2("datasets/choice_dataset_perceived_choices.csv", header=T,dec=".",sep=",")

corr<-function(df, x){ # plot correlation table funntion
  corel = df
  M = cor(corel)
  testRes=cor.mtest(corel, conf.level=x)
  corrplot(M, method = 'number', p.mat = testRes$p, sig.level = 1-x, diag=FALSE)} 

corr(subset(data1, select=c(binchoice1, cartime, carcost, carpsafe, young, gender)), 0.95)
corr(subset(data1, select=c(binchoice2, acttime, ebikecost, ebikepsafe, young, gender)), 0.95)
corr(subset(data1, select=c(binchoice3, acttime, escootcost, escootpsafe, young, gender)), 0.95)
corr(subset(data1, select=c(binchoice4, acttime, walkpsafe, young, gender)), 0.95)

# descriptive statistics related with sociodemographic characteristics...
summary(as.factor(subset(data1, gender==1)$binchoice1)) # male who select car
summary(as.factor(subset(data1, gender==1)$binchoice2)) # male who select ebike
summary(as.factor(subset(data1, gender==1)$binchoice3)) # male who select e-scoot
summary(as.factor(subset(data1, gender==1)$binchoice4)) # male who select walk

summary(as.factor(subset(data1, gender==0)$binchoice1)) # female who select car
summary(as.factor(subset(data1, gender==0)$binchoice2)) # female who select ebike
summary(as.factor(subset(data1, gender==0)$binchoice3)) # female who select e-scoot
summary(as.factor(subset(data1, gender==0)$binchoice4)) # female whoi select walk

summary(as.factor(subset(data1, young==1)$binchoice1)) # young who select car
summary(as.factor(subset(data1, young==1)$binchoice2)) # young who select ebike
summary(as.factor(subset(data1, young==1)$binchoice3)) # young who select e-scoot
summary(as.factor(subset(data1, young==1)$binchoice4)) # young who select walk

summary(as.factor(subset(data1, young==0)$binchoice1)) # not young who select car
summary(as.factor(subset(data1, young==0)$binchoice2)) # not young who select ebike
summary(as.factor(subset(data1, young==0)$binchoice3)) # not young who select e-scoot
summary(as.factor(subset(data1, young==0)$binchoice4)) # not young who select walk


hist_choices <- function(df, fi, x, tit){
  p<-ggplot(df, aes(fill = factor({{fi}}), x = factor({{x}}))) + 
    geom_bar(stat = "count", position = "fill") + 
    scale_fill_brewer(palette = 'Set1', name = "Choice", 
                      labels = c('0: not use', '1: use')) +
    scale_x_discrete(name =tit) +
    scale_y_continuous(name ="Percentage of responces (%)", 
                       labels = function(x) paste0(x*100, "%")) + theme_bw() + coord_flip() +
    geom_text(aes(label = scales::percent(..count../tapply(..count.., ..x.. ,sum)[..x..], accuracy = 0.1)),
              position = position_fill(vjust = 0.5),
              stat = "count")
  return(p)}

# car
p1<-hist_choices(data1, binchoice1, cartime, 'Travel time in minutes') + ggtitle('car')
p2<-hist_choices(data1, binchoice1, carcost, 'Trip cost in euros') + ggtitle('car')
p3<-hist_choices(data1, binchoice1, carpsafe, 'Perceived Safety level') + ggtitle('car')

# ebike
p4<-hist_choices(data1, binchoice2, acttime, 'Travel time in minutes') + ggtitle('e-bike')
p5<-hist_choices(data1, binchoice2, ebikecost, 'Trip cost in euros') + ggtitle('e-bike')
p6<-hist_choices(data1, binchoice2, ebikepsafe, 'Perceived Safety level') + ggtitle('e-bike')

# escooter
p7<-hist_choices(data1, binchoice3, round((20/15) * acttime, digits = 0), 'Travel time in minutes') + ggtitle('e-scooter')
p8<-hist_choices(data1, binchoice3, escootcost, 'Trip cost in euros') + ggtitle('e-scooter')
p9<-hist_choices(data1, binchoice3, escootpsafe, 'Perceived Safety level') + ggtitle('e-scooter')

# walk
p10<-hist_choices(data1, binchoice4, (20/5)*acttime, 'Travel time in minutes') + ggtitle('walk')
p11<-ggplot()+geom_blank() + theme_bw()
p12<-hist_choices(data1, binchoice4, walkpsafe, 'Perceived Safety level') + ggtitle('walk')

ggarrange(p1, p2, p3,
          p4, p5, p6, 
          p7, p8, p9,
          p10, p11, p12, ncol = 3, nrow = 4, common.legend = TRUE, legend = 'bottom')

