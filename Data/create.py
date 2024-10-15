import csv
import psycopg2

class NamesAPI:
    connection = []
    cursor = []
    
    def __init__(self) -> None:
        """
         makes connection and cursor for queries
        """
        self.connection = psycopg2.connect(database="clinecolee", user="clinecolee", password="happy449berry", host="localhost")
        self.cursor = self.connection.cursor()
        print("PostgreSQL connection is opened")

    def close(self) -> None:
        """
        Closes cursor and connection to queries
        """
        self.cursor.close()
        self.connection.close()
        print("PostgreSQL connection is closed")

    def create_table(self):
        """
        Creates the names table in the database
        """
        create_table_query = """
        DROP TABLE IF EXISTS names;
        CREATE TABLE names (
            _year int,
            _name text,
            sex text,
            amount int
        );
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()
        print("Table is created")

    def load_csv_to_db(self, csv_file_path: str) -> None:
        """
        Loads the CSV file into the PostgreSQL names table
        """
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row if it exists
            for row in reader:
                self.cursor.execute(
                    "INSERT INTO names (_year, _name, sex, amount) VALUES (%s, %s, %s, %s)",
                    row
                )
        self.connection.commit()
        print("CSV data has been loaded into the database")

if __name__ == '__main__':
    api = NamesAPI()
    api.create_table()  # Creates the table
    api.load_csv_to_db('ls /Users/xzj/Documents/GitHub/Normalist_Name/Data/all_years.csv')  # Replace with your CSV file path
    api.close()
