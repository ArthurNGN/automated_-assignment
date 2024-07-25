import pandas as pd
import logging

def process_movie_genres_df(df, output_file):
    # Create a new DataFrame for the triples
    triples = []

    # Log the processing of the movies
    logging.info(f"Processing {len(df)} movies")

    # Loop through each row in the DataFrame to create triples
    for index, row in df.iterrows():
        movie_id = row['movie_id']
        genres = row['genres'].split('|')

        # Create triples for each genre
        for genre in genres:
            triples.append((movie_id, 'belongs_to', genre))

    # Convert the list of triples to a DataFrame
    triples_df = pd.DataFrame(triples, columns=['subject', 'predicate', 'object'])

    # Save the triples to a CSV file with header
    triples_df.to_csv(output_file, index=False, header=True)

    logging.info(f"Genre triples saved to {output_file}\n")

    return triples_df
