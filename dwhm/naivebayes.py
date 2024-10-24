import pandas as pd
import numpy as np

df = pd.DataFrame({
    'income': ['very high', 'high', 'medium', 'high', 'very high', 'medium', 'high', 'medium', 'high', 'low'],
    'credit': ['excellent', 'good', 'excellent', 'good', 'good', 'excellent', 'bad', 'bad', 'bad', 'bad' ],
    'decision': ['authorize', 'authorize', 'authorize', 'authorize', 'authorize', 'authorize', 'request id', 'request id', 'reject', 'call police']
})



p_of_authorize = df['decision'].value_counts()['authorize'] / len(df)
print("c1 probability:",p_of_authorize)

p_of_request_id = df['decision'].value_counts()['request id'] / len(df)
print("c2 probablity:",p_of_request_id)

p_of_reject = df['decision'].value_counts()['reject'] / len(df)
print('c3 probability:',p_of_reject)

p_of_call_police = df['decision'].value_counts()['call police'] / len(df)
print('c4 probablitiy:',p_of_call_police)

tuple_to_add = ('medium', 'good')

p_of_x_on_c1 = df['income'].value_counts()['medium'] / df['decision'].value_counts()['authorize'] + df['credit'].value_counts()['good'] / df['decision'].value_counts()['authorize']

print(p_of_x_on_c1)

p_of_x_on_c2 = df['income'].value_counts()['medium'] / df['decision'].value_counts()['request id'] + df['credit'].value_counts()['good'] / df['decision'].value_counts()['authorize']

p_of_x_on_c3 = df['income'].value_counts()['medium'] / df['decision'].value_counts()['authorize'] + df['credit'].value_counts()['good'] / df['decision'].value_counts()['authorize']

p_of_x_on_c4 = df['income'].value_counts()['medium'] / df['decision'].value_counts()['authorize'] + df['credit'].value_counts()['good'] / df['decision'].value_counts()['authorize']


p_of_c1_on_x = p_of_authorize*p_of_x_on_c1
p_of_c2_on_x = p_of_request_id*p_of_x_on_c2
p_of_c3_on_x = p_of_reject*p_of_x_on_c3
p_of_c4_on_x = p_of_call_police*p_of_x_on_c4

posterior_probabilities = [p_of_c1_on_x, p_of_c2_on_x, p_of_c3_on_x, p_of_c4_on_x]

max_prob = max(max(max(p_of_c1_on_x, p_of_c2_on_x), p_of_c3_on_x), p_of_c4_on_x)
print(f"maximum posterior probability is {max_prob}")

for probability in posterior_probabilities:
  i = 1
  if max_prob == probability:
    print(f"tuple classified into c{i}")
    break
  i += 1





