import torch
import pandas as pd

# Load entity embeddings
embeddings = torch.load('model/embeddings_entity_0.v0.pt')

# Load entity names
entity_names = pd.read_csv('data/entity_names_all_0.tsv', sep='\t', header=None)[0]

# Convert to DataFrame
embedding_df = pd.DataFrame(embeddings.numpy(), index=entity_names)

# Save to CSV
embedding_df.to_csv('entity_embeddings.csv')
