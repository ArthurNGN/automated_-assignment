import pandas as pd
from transformers import BartTokenizer, BartForConditionalGeneration
import nltk
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Download the NLTK Punkt tokenizer models (used for sentence tokenization)
nltk.download('punkt')

# Load BART tokenizer and model for conditional generation (using IBM model)
tokenizer = BartTokenizer.from_pretrained("ibm/knowgl-large")
model = BartForConditionalGeneration.from_pretrained("ibm/knowgl-large")

# Function to process movie plot and generate triples
def process_movie_plot(movie_plot):
    # Tokenize the movie plot into sentences
    sentences = nltk.sent_tokenize(movie_plot)
    
    all_triples = set()  # Use a set to avoid duplicates

    # Process each sentence individually
    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", max_length=1024, truncation=True, padding="max_length")
        outputs = model.generate(**inputs)
        decoded_triples = tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        all_triples.update(decoded_triples)

    # Process pairs of consecutive sentences
    for i in range(len(sentences) - 1):
        concatenated_sentences = sentences[i] + " " + sentences[i + 1]
        inputs = tokenizer(concatenated_sentences, return_tensors="pt", max_length=1024, truncation=True, padding="max_length")
        outputs = model.generate(**inputs)
        decoded_triples = tokenizer.batch_decode(outputs, skip_special_tokens=True, clean_up_tokenization_spaces=True)
        all_triples.update(decoded_triples)
    
    # Concatenate all triples with the dollar ($) separator and remove sep char (,)
    triples_str = "$".join(all_triples).replace(',', '')

    return triples_str

# Function to process a single movie row
def process_single_movie(row):
    try:
        movie_id = str(row["movie_id"])
        title = row["title"]
        movie_plot = row["plot"]
        logging.info(f"Processing movie id: {movie_id}, title: {title}")
        triples = process_movie_plot(movie_plot)
        return (movie_id, title, triples)
    except Exception as e:
        logging.error(f"Error processing movie_id {row['movie_id']}: {str(e)}")
        return None

def process_movie_df(df, threads, output_csv_file_name):
    # Load existing output file if it exists
    processed_movie_ids = set()
    if os.path.exists(output_csv_file_name):
        processed_df = pd.read_csv(output_csv_file_name)
        processed_movie_ids = set(processed_df["movie_id"].astype(str))

    # Filter out already processed movies
    rows_to_process = df[~df["movie_id"].astype(str).isin(processed_movie_ids)]
    logging.info(f"Threads: {threads} ; Rows to process: {len(rows_to_process)}")

    # Use ThreadPoolExecutor to process multiple movies concurrently
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_row = {executor.submit(process_single_movie, row): row for index, row in rows_to_process.iterrows()}

        # Check if the file exists to determine if we need to write the header
        file_exists = os.path.exists(output_csv_file_name)
        
        with open(output_csv_file_name, 'a') as f:
            if not file_exists:
                f.write("movie_id,title,triples\n")

            for future in as_completed(future_to_row):
                result = future.result()
                if result:
                    movie_id, title, triples = result
                    f.write(f"{movie_id},{title},{triples}\n")
                    logging.info(f"Processed movie id: {movie_id}, title: {title}")

    # Log completion message
    logging.info("Script completed processing all rows.")

    # Remove checkpoint file after successful completion (optional)
    checkpoint_file = 'ml-1m/checkpoint.pth'
    if os.path.exists(checkpoint_file):
        os.remove(checkpoint_file)

    logging.info(f"DataFrame saved in {output_csv_file_name}\n")
