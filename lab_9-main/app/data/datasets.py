def insert_dataset(dataset_name, category, source, last_updated,
                   record_count, file_size_mb):
    """Insert a new dataset record."""
    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO datasets_metadata
        (dataset_name, category, source, last_updated,
         record_count, file_size_mb)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dataset_name, category, source, last_updated,
          record_count, file_size_mb))

    conn.commit()
    dataset_id = cursor.lastrowid
    conn.close()

    return dataset_id


def get_all_datasets():
    """Return all datasets as a DataFrame."""
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM datasets_metadata", conn)
    conn.close()
    return df
