import os
import csv
import glob
import pymysql

def setup_mysql():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_dir = os.path.join(base_dir, 'Text to SQL', 'Data_CSV')
    
    try:
        # Connect without db to create schema
        conn = pymysql.connect(host='localhost', user='root', password='root')
        with conn.cursor() as cur:
            cur.execute("CREATE DATABASE IF NOT EXISTS text_to_sql")
            cur.execute("USE text_to_sql")
            print("Database text_to_sql selected.")
            
            csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))
            for file_path in csv_files:
                table_name = os.path.basename(file_path).replace('.csv', '').lower()
                print(f"Ingesting {table_name} into MySQL...")
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.reader(f)
                    headers = next(reader)
                    
                    # Sanitize headers
                    headers = [h.strip().replace(' ', '_').replace('.', '_') for h in headers]
                    cols = ", ".join([f'`{h}` TEXT' for h in headers])
                    
                    cur.execute(f'DROP TABLE IF EXISTS `{table_name}`')
                    cur.execute(f'CREATE TABLE `{table_name}` ({cols})')
                    
                    placeholders = ", ".join(["%s"] * len(headers))
                    insert_query = f'INSERT INTO `{table_name}` VALUES ({placeholders})'
                    
                    rows = []
                    for row in reader:
                        if len(row) < len(headers):
                            row += [''] * (len(headers) - len(row))
                        elif len(row) > len(headers):
                            row = row[:len(headers)]
                        rows.append(row)
                        
                    cur.executemany(insert_query, rows)
                    conn.commit()
                print(f"Loaded {len(rows)} rows into {table_name}.")
    except Exception as e:
        print(f"MySQL Error: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    setup_mysql()
