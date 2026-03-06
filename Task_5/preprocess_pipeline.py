import pandas as pd
import logging
import time
import os

# -----------------------------
# Logging Configuration
# -----------------------------
logging.basicConfig(
    filename="preprocessing_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_data(file_path):
    """Load dataset"""
    try:
        df = pd.read_csv(file_path)
        logging.info("Dataset loaded successfully")
        return df
    except Exception as e:
        logging.error(f"Error loading dataset: {e}")
        raise

def standardize_columns(df):
    """Convert column names to lowercase"""
    df.columns = df.columns.str.lower()
    logging.info("Column names standardized to lowercase")
    return df

def handle_missing_values(df):
    """Handle missing values and clean user_score"""
    
    # Fill missing year_of_release with 0
    if 'year_of_release' in df.columns:
        df['year_of_release'] = df['year_of_release'].fillna(0)

    # Convert 'tbd' to NaN
    if 'user_score' in df.columns:
        df['user_score'] = df['user_score'].replace('tbd', pd.NA)
        df['user_score'] = pd.to_numeric(df['user_score'], errors='coerce')

    logging.info("Missing values handled successfully")
    
    return df

def drop_invalid_rows(df):
    """Drop rows with critical missing values"""
    
    initial_rows = len(df)
    
    if 'critic_score' in df.columns and 'user_score' in df.columns:
        df = df.dropna(subset=['critic_score','user_score'])
    
    final_rows = len(df)
    
    logging.info(f"Rows before cleaning: {initial_rows}")
    logging.info(f"Rows after cleaning: {final_rows}")
    
    return df, final_rows

def save_clean_data(df, output_file):
    """Save cleaned dataset"""
    
    df.to_csv(output_file, index=False)
    logging.info(f"Clean dataset saved as {output_file}")

def main():

    start_time = time.time()
    
    logging.info("Preprocessing pipeline started")

    dataset_path = "games(1).csv"
    output_file = "games_cleaned.csv"

    df = load_data(dataset_path)
    
    df = standardize_columns(df)
    
    df = handle_missing_values(df)
    
    df, rows_processed = drop_invalid_rows(df)
    
    save_clean_data(df, output_file)

    runtime = round(time.time() - start_time, 2)

    logging.info(f"Total rows processed: {rows_processed}")
    logging.info(f"Pipeline runtime: {runtime} seconds")
    logging.info("Preprocessing pipeline completed successfully")

    print("Preprocessing completed successfully")
    print(f"Rows processed: {rows_processed}")
    print(f"Runtime: {runtime} seconds")

if __name__ == "__main__":
    main()