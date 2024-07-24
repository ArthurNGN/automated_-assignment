import pandas as pd
import logging

def process_film_registry(input_csv_file_names, column_dict, output_csv_file_name):
    
    try:
        logging.info(f"Reading data from source files: {[name.split('/')[-1] for name in input_csv_file_names]}")
        
        # Read all CSV files into a list of DataFrames
        dataframes = []
        for file_name in input_csv_file_names:
            try:
                df = pd.read_csv(file_name)
                dataframes.append(df)
                logging.info(f"Successfully read {file_name.split('/')[-1]}")
            except Exception as e:
                logging.error(f"Error reading {file_name}: {e}")
                return None
        
        # Merge all DataFrames on their common columns
        if len(dataframes) > 1:
            merged_df = dataframes[0]
            for df in dataframes[1:]:
                merge_cols = list(set(merged_df.columns).intersection(set(df.columns)))
                merged_df = pd.merge(merged_df, df, on=merge_cols, how='inner')
                logging.info(f"Merge successfull using {merge_cols} columns")
        else:
            merged_df = dataframes[0]
        
        # Sélection des colonnes souhaitées
        film_registry_selected = merged_df[list(column_dict.keys())]
        
        # Renommage des colonnes
        film_registry_selected = film_registry_selected.rename(columns = column_dict)

        if 'title' in column_dict.values() :
            # Décompte des valeurs non nulles et non vides avant transformation
            count_before = film_registry_selected['title'].notnull().sum() - (film_registry_selected['title'] == '').sum()
            logging.info(f"STD- Title count: {count_before}")

            # Nettoyage des titres pour enlever les chaînes après '(' ou ','
            film_registry_selected['title'] = film_registry_selected['title'].str.split('(').str[0].str.split(',').str[0].str.strip()

            # Décompte des valeurs non nulles et non vides après transformation
            count_after = film_registry_selected['title'].notnull().sum() - (film_registry_selected['title'] == '').sum()
            logging.info(f"STD+ Title count: {count_after}")
        else :
            logging.info(f"No title column found")
        
        # Sauvegarde du DataFrame dans un fichier CSV (remplace s'il existe déjà)
        film_registry_selected.to_csv(output_csv_file_name, index=False)
        logging.info(f"DataFrame saved in {output_csv_file_name}\n")
        
        return film_registry_selected
    
    except Exception as e:
        logging.error(f"Une erreur est survenue: {e}\n")
        return None

if __name__ == "__main__":
    df = process_film_registry()
