"""
api.py

Python API for team-d:
For CS257 W24

Ethan Cline-Cole, Ben Sherrick, Harry Xun

"""

import random
import csv
import psycopg2



class NamesAPI:
    connection = []
    cursor = []
    
    def __init__(self) -> None:
        """
         makes connection and cursor for queries
        """
        self.connection = psycopg2.connect(database="clinecolee",user="clinecolee",password="happy449berry",host="localhost")
        self.cursor = self.connection.cursor()
        print("PostgreSQL connection is opened")

    def close(self) -> None:
        """
        Closes cursor and connection to queries
        """
        self.cursor.close()
        self.connection.close()
        print("PostgreSQL connection is closed")

    def validate_input_year(self, year, lower_bound_popularity, upper_bound_popularity) -> bool:
        """
        Validates the input parameters for the generate_name_from function.

        Parameters:
        - year: The year for which names are being generated.
        - lower_bound_popularity: The lower bound popularity for filtering names.
        - upper_bound_popularity: The upper bound popularity for filtering names.

        Returns:
        - True if input is valid, False otherwise.
        """
        if year < 1880 or year > 2022:
            print("Invalid year. Database ranges from 1880-2022")
            return False

        if lower_bound_popularity < 0 or upper_bound_popularity < 0 or lower_bound_popularity > upper_bound_popularity:
            print("Wrong input: invalid popularity.")
            return False

        else: 
            return True
        
    def validate_input_name(self, name: str) -> bool:
        """
        Checks if the input name exists within the database.

        Parameters:
        - name: The name to be checked.

        Returns:
        - True if the name exists in the database, False otherwise.
        """
        self.cursor.execute("SELECT COUNT(*) FROM names WHERE _name = %s", (name,))
        result = self.cursor.fetchone()
        name_count = result[0]

        if name_count > 0:
            return True
        else:
            return False

    def get_random_year_of_name(self, name) -> int:
        """
        Returns a random year in which the given name appears in the database.
        """
        self.cursor.execute("SELECT DISTINCT _year FROM names WHERE _name = %s", (name,))
        years = self.cursor.fetchall()

        if years:
            return random.choice([year[0] for year in years])
        else:
            print(f"No data found for the name {name}.")
            return -1 


    def get_close_name(self, name, year):
        """
        Returns a name that is close in popularity to the given name in the specified year,
        ensuring it is different from the input name.
        """
        self.cursor.execute("""
            SELECT row_number() OVER (ORDER BY amount DESC) AS rownum 
            FROM names 
            WHERE _year = %s AND _name = %s
        """, (year, name))
    
        result = self.cursor.fetchone()

        if result:
            name_rank = result[0]
            total_names = self.get_total_names_count(year)

            while True:
                close_rank = name_rank + random.randint(-50, 50)
            
                close_rank = max(1, min(close_rank, total_names)) - 1

                self.cursor.execute("""
                    SELECT _name 
                    FROM names 
                    WHERE _year = %s 
                    ORDER BY amount DESC
                    LIMIT 1 OFFSET %s
                """, (year, close_rank))
            
                close_name = self.cursor.fetchone()

                if close_name and close_name[0] != name:
                    return close_name[0]
        return -1
    
    def get_total_names_count(self, year):
        """
        Returns the total number of names in the database for a given year.
        """
        self.cursor.execute("""
            SELECT COUNT(*) 
            FROM names 
            WHERE _year = %s
        """, (year,))

        result = self.cursor.fetchone()
        return result[0] if result else -1

    def get_popularity_of(self, name, year) -> int:
        """
        For any given string name and given year, the function will return the count of 
        people using that name in that year.
        If the year is not between 1880-2022, return “-1"
        If the name does not exist in the database, returns 0
        Returns total for male and female
        """
        # validating year and name input
        if not self.validate_input_year(year, 0, 1):
           return -1
        if not self.validate_input_name(name):
            print("Name does not exist in the database.")
            return -1
                
        self.cursor.execute("SELECT amount FROM names WHERE _year = %s AND _name =\'%s\';" % (year, name))
        result = self.cursor.fetchall()
        amount = 0
        for i in result:
            amount += i[0]
        return amount
                
        # user role: An expecting parent trying to find a unique name that is not too uncommon.
        # Cases: (!) Name is string, (!) year is in range, (!) year is int

    def generate_name_from(self, lower_bound_year, upper_bound_year, lower_bound_popularity, upper_bound_popularity):
        """
        For the given year, the function will give the names with the n1 to n2 largest amounts,
        where n1 is the lower_bound_popularity and n2 is the upper_bound_popularity,
        ordered by popularity in descending order.
        If the year is not between 1880-2022, return “Invalid year. Database ranges from 1880-2022”
        If lower_bound_popularity is negative or upper_bound_popularity is negative or lower_bound_popularity is higher than upper_bound_popularity, return “Wrong input: invalid popularity.”
        If there is no name between the given popularity, return “Sorry, there is no name between your given popularities in that year.”
        """
        # Validate input years and popularity bounds
        if not self.validate_input_year(lower_bound_year, lower_bound_popularity, upper_bound_popularity) or \
        not self.validate_input_year(upper_bound_year, lower_bound_popularity, upper_bound_popularity):
            return -1

        # Calculate the offset and limit for the query
        offset = lower_bound_popularity - 1  # Offset is 0-indexed
        limit = upper_bound_popularity - lower_bound_popularity + 1

        # Construct and execute the SQL query to fetch names with the n1 to n2 largest amounts
        query = """SELECT _name FROM names WHERE _year BETWEEN %s AND %s ORDER BY amount DESC OFFSET %s LIMIT %s;"""
        self.cursor.execute(query, (lower_bound_year, upper_bound_year, offset, limit))
        names_list = self.cursor.fetchall()

        # Check if any names are found within the popularity bounds
        if not names_list:
            print("Sorry, there is no name between your given popularities in that year.")
            return -1

        # Return the list of names
        return [name[0] for name in names_list]
        # user role: A historical writer trying to find unique names for the characters that fit historical settings


    def get_sex_ratio(self, name, year) -> float:
        """
        For any given string name, int year, and string sex, return a float percentage of people from the year that had the name ‘name’ who are male -> 0.0 (only female) -> 1.0 (only male)
        If the year is not between 1880-2022, return “Invalid year. Database ranges from 1880-2022”
        If the name does not exist in the database, return “Name does not exist in database”
        """
        # validating year and name input
        if not self.validate_input_year(year, 0, 1):
           return -1
        if not self.validate_input_name(name):
            print("Name does not exist in the database.")
            return -1
        
        maleCount = 0.0
        femaleCount = 0.0
        self.cursor.execute("SELECT amount FROM names WHERE _name = '%s' AND _year = %s AND sex = 'M';" % (name, year))
        found = self.cursor.fetchall()
        if found:
            maleCount = found[0][0]
        self.cursor.execute("SELECT amount FROM names WHERE _name = '%s' AND _year = %s AND sex = 'F';" % (name, year))
        found = self.cursor.fetchall()
        if found:
            femaleCount = found[0][0]

        if maleCount + femaleCount == 0.0:
            return -1
        return (maleCount) / (maleCount + femaleCount)

        # Cases: (!) Name is string, (!) year is in range, (!) year is int
        # user role: student doing a project on gender-neutral names and their history
    
    def generate_name_from_partial(self, partial: str):
        """
        Returns the complete list of names that contain the string partial within the name.
        If partial does not exist in any names in the database, return “No names containing your string exist”
        """
        trimmed_name_list = []
        self.cursor.execute("SELECT DISTINCT _name FROM names WHERE _name LIKE \'%s\';" % (partial.capitalize() + "%"))
        nameList = self.cursor.fetchall()
        for n in nameList:
            trimmed_name_list.append(n[0])
        # user role: Someone wanting to name their child after a person/thing
        return trimmed_name_list
        # Cases: (!) Name is string, (!) Partial is string
    

    def Get_Most_Used_Year_Of(self, name):
        """
        This function returns the year when the input name is most commonly used.
        If the name does not exist in the database, return “Uncommon name”
        """
        current_best_sum = -1
        current_best_year = -1
        self.cursor.execute("SELECT _year, amount FROM names WHERE _name = %s ORDER BY amount DESC LIMIT 1", (name,))
        result = self.cursor.fetchone()
    
        # If the name does not exist in the database, return "Uncommon name"
        if result is None:
            print("Name does not exist in the database.")
            return -1
    
        current_best_year = result[0]
        current_best_sum = result[1]

        return current_best_year

if __name__ == "__main__":
    nameFinder = NamesAPI()
    print("popularity of Robert year 2000")
    print(nameFinder.get_popularity_of("Robert",2000))
    print("get name with 40000 occurances from 2008-2010")
    print(nameFinder.generate_name_from(2008,2010, 3905,4000))
    print("Get Names that start with Henr")
    print(nameFinder.generate_name_from_partial("Henr"))
    print("Get Name Sex Ratio of Joan 2019")
    print(nameFinder.get_sex_ratio("Joan",2019))
    print("Get most used year of Doug")
    print(nameFinder.Get_Most_Used_Year_Of("Doug"))
    print("Name of similar popularity to Harry")
    print(nameFinder.get_close_name("Harry",1988))
#    nameFinder.play_game()

    nameFinder.close()
    
    
        
