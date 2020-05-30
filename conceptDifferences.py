import pandas as pd

actual_concepts = pd.read_csv("data\\actual_concepts.csv", dtype={'icao24': str, 'arriving': bool}).sort_values(by=["timestamp"])
expected_concepts = pd.read_csv("data\\expected_concept_V3Final.csv").sort_values(by=["timestamp"])

# actual_concepts = ['timestamp'].str.rstrip('.!? \n\t')

zeroes = pd.DataFrame(["+00:00"]*len(expected_concepts))

#expected_concepts["timestamp"] = expected_concepts["timestamp"].str.cat(zeroes, sep ="")

# concepts = actual_concepts.append(expected_concepts['ExpectedConcept'])
# print(concepts)

result = pd.merge(actual_concepts, expected_concepts, how='inner', on='flight_id')

result = result.drop(columns=['heading', 'timestamp_y', 'next_concept', 'match'])

result.rename(columns={'concept':'possible_concept',
                          'timestamp_x':'timestamp',
                          'ExpectedConcept':'scheduled_concept',
                       'runway':'initial_runway'},
                 inplace=True)

result = result[['timestamp', 'scheduled_concept', 'current_concept', 'possible_concept',
                 'initial_runway', 'new_runway', 'flight_id', 'icao24', 'arriving']]

result.to_csv('data\\concept_analysis.csv', index = False)

print('finished.')