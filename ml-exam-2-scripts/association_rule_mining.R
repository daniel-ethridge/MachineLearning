library(arules)
library(arulesViz)
library(RColorBrewer)

# Set path
setwd(dirname(rstudioapi::getSourceEditorContext()$path))

df_name <- "./data/"

# Read in the transactions
arm_transactions <- arules::read.transactions(df_name,
                                               rm.duplicates = FALSE, 
                                               format = "basket",
                                               sep=",",
                                               cols=NULL)

# Perform Apriori to get the rules
arm_rules <- arules::apriori(arm_transactions, parameter = list(support=0.01, 
                                                          confidence=0.5, 
                                                          minlen=2)) |> 
  sort(by="lift")

inspect(arm_rules)

arules::itemFrequencyPlot(arm_transactions,
                          topN = 20,
                          col = brewer.pal(8, 'Pastel2'),
                          main = 'Relative Item Frequency Plot',
                          type = "relative", #absolute
                          ylab = "Item Frequency (Relative)")

# Perform Apriori to get the rules
arm_rules <- arules::apriori(arm_transactions, parameter = list(support=0.01, 
                                                                confidence=0.5, 
                                                                minlen=2),
                             appearance = list(default = "rhs", lhs = "")) |> 
  sort(by="lift")

inspect(arm_rules)

plot(female_vocalist, method="graph")
