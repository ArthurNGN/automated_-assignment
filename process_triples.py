import pandas as pd
import logging
import csv

def parse_triples(movie_id, triples):
    parsed_triples = []
    for i, triple_str in enumerate(triples.split("$")):
        try:
            # Remove the outer brackets and split by the pipe character
            triple_parts = triple_str.strip()[1:-1].split("|")
            if len(triple_parts) != 3:
                raise ValueError(f"Unexpected triple format: {triple_str}")

            parsed_triples.append((triple_parts[0], triple_parts[1], triple_parts[2]))
        except Exception as e:
            print(f"Error parsing triple for movie_id {movie_id}: {triple_str}: {e}")
    return parsed_triples

def generate_graph(movie_id, triples):
    graph = []
    parsed_triples = parse_triples(movie_id, triples)
    subjects_objects = set()
    for triple in parsed_triples:
        subjects_objects.add(triple[0])
        subjects_objects.add(triple[2])
        graph.append((triple[0], triple[1], triple[2]))
    for item in subjects_objects:
        graph.append((movie_id, "contains", item))
    return graph

def process_triples_df(df, output_csv_file_name):
    # Create a list to store the processed rows
    processed_data = []

    logging.info(f"Loading Triples")

    for index, row in df.iterrows():
        movie_id = row['movie_id']
        title = row['title']
        old_triples = row['triples']
        graph = generate_graph(movie_id, old_triples)

        # Create the new triples for the graph
        triples = '$'.join([f"[{old_triples[0]}|{old_triples[1]}|{old_triples[2]}]" for old_triples in graph])

        # Append the processed row to the list
        processed_data.append([movie_id, title, triples])

    # Convert the processed data into a DataFrame
    processed_df = pd.DataFrame(processed_data, columns=['movie_id', 'title', 'triples'])

    logging.info(f"{len(processed_df)} triples successfully processed")

    processed_df.to_csv(output_csv_file_name, index=False)  # Save the processed data to a new CSV file

    logging.info(f"DataFrame saved in {output_csv_file_name}\n")
    return processed_df
