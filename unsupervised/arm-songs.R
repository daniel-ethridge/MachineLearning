library(arules)
library(arulesViz)
library(RColorBrewer)
library(rCBA)

# Set path
setwd(dirname(rstudioapi::getSourceEditorContext()$path))

song_tags <- arules::read.transactions("./../unsynced-data/lastfm-clean-tags-reduced.csv",
                                               rm.duplicates = FALSE, 
                                               format = "basket",
                                               sep=",",
                                               cols=NULL)

# Perform Apriori to get the rules
arm <- arules::apriori(song_tags, parameter = list(support=0.01, 
                                                       confidence=0.5, minlen=2)) |> 
  sort(by="lift")

fp <- rCBA::fpgrowth(song_tags)

plot(arm, method="graph")

inspect(arm)

arules::itemFrequencyPlot(song_tags,
                          topN = 20,
                          col = brewer.pal(8, 'Pastel2'),
                          main = 'Relative Item Frequency Plot',
                          type = "relative", #absolute
                          ylab = "Item Frequency (Relative)")

female_vocalist <- apriori(song_tags, 
                           parameter = list(support=0.01, 
                                            confidence=0.1,
                                            minlen=2),
                           appearance = list(default="rhs", lhs="female vocalist")) |> 
  sort(by="lift")
inspect(female_vocalist)

female_vocalist <- apriori(song_tags, 
                           parameter = list(support=0.01, 
                                            confidence=0.2,
                                            minlen=2),
                           appearance = list(default="lhs", rhs="female vocalist")) |> 
  sort(by="lift")
inspect(female_vocalist)

plot(female_vocalist, method="graph")

male_vocalist <- apriori(song_tags, 
                           parameter = list(support=0.01, 
                                            confidence=0.2,
                                            minlen=2),
                           appearance = list(default="rhs", lhs="male vocalist")) |> 
  sort(by="lift")
inspect(male_vocalist)

male_vocalist <- apriori(song_tags, 
                         parameter = list(support=0.01, 
                                          confidence=0.2,
                                          minlen=2),
                         appearance = list(default="lhs", rhs="male vocalist")) |> 
  sort(by="lift")

plot(male_vocalist, method="graph")


