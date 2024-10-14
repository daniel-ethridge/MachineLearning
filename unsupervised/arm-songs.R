# library(viridis)
library(arules)
# library(TSP)
# library(data.table)
# 
# library(tcltk)
# library(dplyr)
# library(devtools)
# library(purrr)
# library(tidyr)
# 
library(arulesViz)
library(RColorBrewer)

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
  sort(by="confidence")

inspect(arm)

plot(arm_reduced, method="graph")

arules::itemFrequencyPlot(reduced_song_tags,
                          topN = 20,
                          col = brewer.pal(8, 'Pastel2'),
                          main = 'Relative Item Frequency Plot',
                          type = "relative", #absolute
                          ylab = "Item Frequency (Relative)")

female_vocalist <- apriori(reduced_song_tags, 
                           parameter = list(support=0.001, 
                                            confidence=0.3,
                                            minlen=2),
                           appearance = list(default="rhs", lhs="female vocalist")) |> 
  sort(by="lift")
inspect(female_vocalist)

male_vocalist <- apriori(reduced_song_tags, 
                           parameter = list(support=0.01, 
                                            confidence=0.2,
                                            minlen=2),
                           appearance = list(default="lhs", rhs="male vocalist")) |> 
  sort(by="support")
inspect(male_vocalist)

electronic <- apriori(reduced_song_tags, 
                         parameter = list(support=0.01, 
                                          confidence=0.1,
                                          minlen=2),
                         appearance = list(default="lhs", rhs="70s")) |> 
  sort(by="lift")
inspect(electronic)


