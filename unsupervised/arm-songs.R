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

full_song_tags <- arules::read.transactions("./unsynced-data/shrunk-full-tags.csv",
                                        rm.duplicates = FALSE, 
                                        format = "basket",  ##if you use "single" also use cols=c(1,2)
                                        sep=",",  ## csv file
                                        cols=NULL) ## The dataset does not have row numbers

reduced_song_tags <- arules::read.transactions("./unsynced-data/shrunk-reduced-tags.csv",
                                               rm.duplicates = FALSE, 
                                               format = "basket",  ##if you use "single" also use cols=c(1,2)
                                               sep=",",  ## csv file
                                               cols=NULL) ## The dataset does not have row numbers

sort_val <- "confidence"

##### Use apriori to get the RULES
arm_full <- arules::apriori(full_song_tags, parameter = list(support=0.02, 
                                                            confidence=0.1, minlen=2)) |> 
  sort(by=sort_val)



##### Use apriori to get the RULES
arm_reduced <- arules::apriori(reduced_song_tags, parameter = list(support=0.001, 
                                                       confidence=0.5, minlen=2)) |> 
  sort(by="confidence")

# inspect(arm_full)
inspectDT(arm_reduced)

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


