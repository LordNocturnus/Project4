import pandas as pd

runway_usage = pd.read_csv("data\\actual_concepts.csv", dtype = {'icao24':str, 'arriving':bool}).sort_values(by=["timestamp"])

print(runway_usage.loc[runway_usage['match']==False])
print(runway_usage.loc[runway_usage['match']==None])

runway_usage.loc[runway_usage['match']==False].to_csv("data\\concept_failures.csv", index=False)