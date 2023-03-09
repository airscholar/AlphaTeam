import json
import pandas as pd
from datetime import datetime

# Read the json file
with open('Dune_Eth_transaction.json') as f:
    data = json.load(f)

# Create a dataframe
df = pd.DataFrame(data)

# convert to string and add 0x
df['from'] = df['from'].apply(lambda x: '0x' + x[2:])
df['to'] = df['to'].apply(lambda x: '0x' + x[2:])

# convert to timestamp
df['block_time'] = df['block_time'].apply(lambda x: int(datetime.strptime(x, '%Y-%m-%dT%H:%M:%S+00:00').timestamp()))

# reorder columns
df = df[['from', 'to', 'value','block_time']]

# write to csv
df.to_csv('Dune_Eth_transaction.csv', index=False)

