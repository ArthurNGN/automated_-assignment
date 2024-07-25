import pandas as pd
import logging

def process_movie_rating_df(df, output_file):
    # Create a new DataFrame for the triples
    triples = []

    # Log the processing of the movie ID
    logging.info(f"Processing {len(df)} movies")

    # Loop through each row in the DataFrame to create triples
    for index, row in df.iterrows():
        user_id = row['user_id']
        movie_id = row['movie_id']
        rating = row['rating']

        # Create triples for user-movie rating relationship
        triples.append((user_id, 'rated', movie_id))
        triples.append((user_id, f'rated_{rating}', movie_id))

    # Convert the list of triples to a DataFrame
    triples_df = pd.DataFrame(triples, columns=['user_id', 'predicate', 'movie_id'])

    # Save the triples to a CSV file
    triples_df.to_csv(output_file, index=False, header=True)

    logging.info(f"Rating triples saved to {output_file}\n")
