import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def init_database():
    # Database configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'local_food_market')

    try:
        # Connect to MySQL server
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' created successfully")

        # Switch to the database
        cursor.execute(f"USE {DB_NAME}")

        # Read and execute schema.sql
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
            # Split into individual statements
            statements = schema_sql.split(';')
            for statement in statements:
                if statement.strip():
                    cursor.execute(statement)
        
        print("Database schema created successfully")

        # Optionally load sample data
        try:
            with open('database/sample_data.sql', 'r', encoding='utf-8') as f:
                sample_data_sql = f.read()
                statements = sample_data_sql.split(';')
                for statement in statements:
                    if statement.strip():
                        cursor.execute(statement)
            print("Sample data loaded successfully")
        except Exception as e:
            print(f"Note: Sample data not loaded: {str(e)}")

        conn.commit()
        print("Database initialization completed successfully")

    except Exception as e:
        print(f"Error initializing database: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    init_database()