import os
import csv
import sqlite3
import glob

def ingest_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_dir = os.path.join(base_dir, 'Text to SQL', 'Data_CSV')
    db_path = os.path.join(base_dir, 'local.db')
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))
    
    if not csv_files:
        print("No CSV files found in", csv_dir)
        return
        
    for file_path in csv_files:
        table_name = os.path.basename(file_path).replace('.csv', '').lower()
        print(f"Ingesting {table_name}...")
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f)
                headers = next(reader)
                
                # Sanitize headers
                headers = [h.strip().replace(' ', '_').replace('.', '_') for h in headers]
                cols = ", ".join([f'"{h}" TEXT' for h in headers])
                
                cur.execute(f'DROP TABLE IF EXISTS "{table_name}"')
                cur.execute(f'CREATE TABLE "{table_name}" ({cols})')
                
                placeholders = ", ".join(["?"] * len(headers))
                insert_query = f'INSERT INTO "{table_name}" VALUES ({placeholders})'
                
                rows = []
                for row in reader:
                    # Pad rows that have missing columns
                    if len(row) < len(headers):
                        row += [''] * (len(headers) - len(row))
                    elif len(row) > len(headers):
                        row = row[:len(headers)]
                    rows.append(row)
                    
                cur.executemany(insert_query, rows)
                conn.commit()
                
            print(f"Successfully loaded {len(rows)} rows into {table_name}.")
        except Exception as e:
            print(f"Failed to load {table_name}: {e}")
            
    conn.close()

if __name__ == "__main__":
    ingest_data()
