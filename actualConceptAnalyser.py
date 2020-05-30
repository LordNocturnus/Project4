import pandas as pd

#runway_usage = pd.read_csv("data\\concept_analysis.csv", dtype = {'icao24':str, 'arriving':bool}).sort_values(by=["timestamp"])

#print(runway_usage.loc[(runway_usage['current_concept']==runway_usage['scheduled_concept'] & runway_usage['scheduled_concept'] != 99)])


actual_concepts = pd.read_csv("data\\actual_concepts.csv", dtype = {'icao24':str, 'arriving':bool}).sort_values(by=["timestamp"])

failed_concepts = actual_concepts.loc[actual_concepts['match'] == False]

failed_concepts = failed_concepts.drop(columns = ['heading'])

failed_concepts.to_csv("data\\concept_failures.csv", index=False)