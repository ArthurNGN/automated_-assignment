import pandas as pd
import os

def preprocess_triples(df):
    # Create directories
    os.makedirs('data/edges', exist_ok=True)

    # Save entities
    entities = pd.concat([df['subject'], df['object']]).unique()
    pd.DataFrame(entities).to_csv('data/entity_names_all_0.tsv', sep='\t', header=False, index=False)

    # Save relations (edges)
    df.to_csv('data/edges/edges_partitioned_0.tsv', sep='\t', header=False, index=False)
