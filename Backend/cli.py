from api import NamesAPI

def main():
    name_finder = NamesAPI()

    print("Welcome to the NamesAPI command line shell!")
    print("Available commands:")
    print("1. get_popularity_of <name> <year>")
    print("2. generate_name_from <lower_bound_year> <upper_bound_year> <lower_bound_popularity> <upper_bound_popularity>")
    print("3. get_sex_ratio <name> <year>")
    print("4. generate_name_from_partial <partial>")
    print("5. Get_Most_Used_Year_Of <name>")
    print("6. Play_Game")
    print("7. quit")
    print("8. help")

    while True:
        user_input = input("Enter a command: ").strip().split()

        if user_input[0] == 'quit':
            break
        elif user_input[0] == 'help':
            print("Available commands:")
            print("1. get_popularity_of <name> <year>")
            print("2. generate_name_from <lower_bound_year> <upper_bound_year> <lower_bound_popularity> <upper_bound_popularity>")
            print("3. get_sex_ratio <name> <year>")
            print("4. generate_name_from_partial <partial>")
            print("5. Get_Most_Used_Year_Of <name>")
            print("6. Play_Game")
            print("7. quit")
            print("8. help")
        elif user_input[0] == 'get_popularity_of':
            name = user_input[1]
            year = int(user_input[2])
            popularity = name_finder.get_popularity_of(name, year)
            if popularity == -1:
                print("Error: Invalid input or name not found")
            else:
                print(popularity)
        elif user_input[0] == 'generate_name_from':
            lower_bound_year = int(user_input[1])
            upper_bound_year = int(user_input[2])
            lower_bound_popularity = int(user_input[3])
            upper_bound_popularity = int(user_input[4])
            names = name_finder.generate_name_from(lower_bound_year, upper_bound_year, lower_bound_popularity, upper_bound_popularity)
            if names == -1:
                print("Error: Invalid input")
            elif not names:
                print("Sorry, there is no name between your given popularities in that year.")
            else:
                print("Names with popularity within the specified range:")
                for name in names:
                    print(name[0])
        elif user_input[0] == 'get_sex_ratio':
            name = user_input[1]
            year = int(user_input[2])
            sex_ratio = name_finder.get_sex_ratio(name, year)
            if sex_ratio == -1:
                print("Error: Invalid input or name not found")
            else:
                print(sex_ratio)
        elif user_input[0] == 'generate_name_from_partial':
            partial = user_input[1]
            names = name_finder.generate_name_from_partial(partial)
            if not names:
                print("No names containing your string exist")
            else:
                print("Names containing the specified string:")
                for name in names:
                    print(name)
        elif user_input[0] == 'Get_Most_Used_Year_Of':
            name = user_input[1]
            most_used_year = name_finder.Get_Most_Used_Year_Of(name)
            if most_used_year == -1:
                print("Error: Invalid input or name not found")
            else:
                print(most_used_year)
        elif user_input[0] == 'Play_Game':
            print("Starting the game...")
            current_name = input("Enter a name to start the game: ")
            score = 0
        
            while True:
                year = name_finder.get_random_year_of_name(current_name)
                if year == -1:
                    print("Name not found in the database. Exiting game.")
                    break
        
                close_name = name_finder.get_close_name(current_name, year)
                if close_name == -1:
                    print("No close names found. Exiting game.")
                    break
        
                print(f"\nYear: {year}")
                print(f"Choose which name was more popular: {current_name} (left) or {close_name} (right)")
        
                choice = input("Enter 'left', 'right', or 'quit' to exit: ").strip().lower()
        
                if choice == 'quit':
                    print("Exiting game.")
                    break
        
                popularity_current = name_finder.get_popularity_of(current_name, year)
                popularity_close = name_finder.get_popularity_of(close_name, year)
        
                if (choice == 'left' and popularity_current > popularity_close) or \
                   (choice == 'right' and popularity_close > popularity_current):
                    print("Correct!")
                    score += 1
                elif (choice == 'left' and popularity_current < popularity_close) or \
                   (choice == 'right' and popularity_close < popularity_current):
                    print("Incorrect!")
                    score -= 1
                else:
                    print("Invalid input.")
        
                print(f"Current score: {score}")
                current_name = close_name if popularity_close > popularity_current else current_name
        
            print(f"Final score: {score}")
        else:
            print("Invalid command. Please try again.")

    name_finder.close()
    print("Exiting NamesAPI command line shell. See u!")

if __name__ == "__main__":
    main()
