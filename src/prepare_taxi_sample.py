from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]

SOURCE = ROOT / "data/raw/yellow_tripdata_2024-01.parquet"
OUTPUT = ROOT / "data/processed/taxi_sample.csv"

COLUMNS = [
    "VendorID",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "PULocationID",
    "DOLocationID",
    "payment_type",
    "fare_amount",
    "total_amount",
]

RENAME = {
    "VendorID": "vendor_id",
    "tpep_pickup_datetime": "pickup_datetime",
    "tpep_dropoff_datetime": "dropoff_datetime",
    "passenger_count": "passenger_count",
    "trip_distance": "trip_distance",
    "PULocationID": "pickup_location_id",
    "DOLocationID": "dropoff_location_id",
    "payment_type": "payment_type",
    "fare_amount": "fare_amount",
    "total_amount": "total_amount",
}


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(f"Dataset absent : {SOURCE}")

    parquet = pq.ParquetFile(SOURCE)
    available = set(parquet.schema_arrow.names)
    missing = set(COLUMNS) - available

    if missing:
        raise ValueError(f"Colonnes absentes du Parquet : {missing}")

    batches = parquet.iter_batches(
        batch_size=5000,
        columns=COLUMNS,
    )

    try:
        batch = next(batches)
    except StopIteration:
        raise ValueError("Le dataset est vide.")

    df = batch.to_pandas().rename(columns=RENAME)

    if df.empty:
        raise ValueError("Aucun trajet dans l'échantillon.")

    df["pickup_datetime"] = pd.to_datetime(
        df["pickup_datetime"], errors="raise"
    )
    df["dropoff_datetime"] = pd.to_datetime(
        df["dropoff_datetime"], errors="raise"
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False, na_rep=r"\N")

    print(f"Lignes : {len(df):,}")
    print(f"Colonnes : {len(df.columns)}")
    print(f"Valeurs manquantes : {int(df.isna().sum().sum())}")
    print(f"CSV créé : {OUTPUT}")
    print(df.head(5).to_string(index=False))


if __name__ == "__main__":
    main()