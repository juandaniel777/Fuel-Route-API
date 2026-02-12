import pandas as pd


def clean_duplicates(input_file, output_file):
    # Load CSV
    df = pd.read_csv(input_file)

    print(f"Total rows before cleaning: {len(df)}")

    # Remove duplicates based on OPIS Truckstop ID
    df_cleaned = df.drop_duplicates(subset=["OPIS Truckstop ID"])

    print(f"Total rows after cleaning: {len(df_cleaned)}")
    print(f"Removed {len(df) - len(df_cleaned)} duplicate rows")

    # Save cleaned file
    df_cleaned.to_csv(output_file, index=False)

    print(f"Cleaned file saved as: {output_file}")


if __name__ == "__main__":
    clean_duplicates(
        "fuel-prices-for-be-assessment.csv",
        "fuel-prices-cleaned.csv"
    )
