import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


low_income = np.random.normal(loc=50000, scale=5000, size=10)
med_income = np.random.normal(loc=100000, scale=10000, size=10)
high_income = np.random.normal(loc=500000, scale=25000, size=10)
incomes = np.concat((low_income, med_income, high_income))
high_spend_1 = np.random.normal(loc=1000, scale=100, size=10)
low_spend = np.random.normal(loc=150, scale=50, size=10)
high_spend_2 = np.random.normal(loc=2000, scale=500, size=10)
spending = np.concat((high_spend_1, low_spend, high_spend_2))

df = pd.DataFrame(data={"annual_income": np.round(incomes),
                        "monthly_spending": np.round(spending)})
df.to_csv("ml-exam4-data.csv")

# The occupation column in the final csv was created manually. Some values in the csv file were edited.