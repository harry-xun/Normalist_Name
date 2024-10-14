from flask import Flask, render_template, request
import sys
from api import NamesAPI

DEFAULT_LOWER_YEAR = 1880
DEFAULT_UPPER_YEAR = 2022
DEFAULT_LOWER_POPULARITY = 1
DEFAULT_UPPER_POPULARITY = 1000
DEFAULT_NAME_COUNT = 10


app = Flask(__name__)
api = NamesAPI()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():    
    if request.method == 'POST':
        lower_bound_year = int(request.form.get('lower_bound_year', DEFAULT_LOWER_YEAR))
        upper_bound_year = int(request.form.get('upper_bound_year', DEFAULT_UPPER_YEAR))
        lower_bound_popularity = int(request.form.get('lower_bound_popularity', DEFAULT_LOWER_POPULARITY))
        upper_bound_popularity = int(request.form.get('upper_bound_popularity', DEFAULT_UPPER_POPULARITY))
        name_count = int(request.form.get('name_count', DEFAULT_NAME_COUNT))

        raw_names = api.generate_name_from(lower_bound_year, upper_bound_year, lower_bound_popularity, upper_bound_popularity)
        if raw_names == -1:
            return render_template('generate.html', 
                                   lower_bound_year=1880,
                                   upper_bound_year=2022,
                                   lower_bound_popularity=1,
                                   upper_bound_popularity=1000,
                                    name_count=30)
        else:
            names = [name[0] for name in raw_names]
            names = names[:name_count]
    else:
        names = []
        lower_bound_year = DEFAULT_LOWER_YEAR
        upper_bound_year = DEFAULT_UPPER_YEAR
        lower_bound_popularity = DEFAULT_LOWER_POPULARITY
        upper_bound_popularity = DEFAULT_UPPER_POPULARITY
        name_count=DEFAULT_NAME_COUNT
        
    return render_template('generate.html', names=names, 
                            lower_bound_year=lower_bound_year,
                           upper_bound_year=upper_bound_year,
                           lower_bound_popularity=lower_bound_popularity,
                           upper_bound_popularity=upper_bound_popularity,
                            name_count=name_count)


@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        choice = request.form.get('choice', '')
        score = int(request.form.get('score', 0))
        current_name = request.form.get('left_name')
        close_name = request.form.get('right_name')
        correct_choice = request.form.get('correct_choice')
        if not current_name:
            current_name = api.get_random_starting_name()
        

        if choice:
            if (choice == correct_choice):
                score += 1
            else:
                score -= 1
                   
        current_name = current_name if correct_choice == 'left' else close_name
        year = api.get_random_year_of_name(current_name)
        if year == -1:
            return render_template('game.html', message="Name not found in the database.")

        close_name = api.get_close_name(current_name, year)
        if close_name == -1:
            return render_template('game.html', message="No close names found.")

        popularity_current = api.get_popularity_of(current_name, year)
        popularity_close = api.get_popularity_of(close_name, year)
        correct_choice = 'left' if popularity_current > popularity_close else 'right'

        return render_template('game.html', 
                               year=year, 
                               left_name=current_name, 
                               right_name=close_name, 
                               score=score,
                               correct_choice=correct_choice)
    else:  
        current_name = api.get_random_starting_name()
        year = api.get_random_year_of_name(current_name)
        close_name = api.get_close_name(current_name, year)
        popularity_current = api.get_popularity_of(current_name, year)
        popularity_close = api.get_popularity_of(close_name, year)
        correct_choice = 'left' if popularity_current > popularity_close else 'right'
        if close_name == -1:
            return render_template('game.html', message="No close names found for the starting name.")

        return render_template('game.html', 
                               year=year, 
                               left_name=current_name, 
                               right_name=close_name, 
                               score=0,
                               correct_choice=correct_choice) 

    return render_template('game.html')
    
@app.route('/search/<name>/', methods=['GET'])
def search(name):
    start_year = DEFAULT_LOWER_YEAR
    end_year = DEFAULT_UPPER_YEAR
    data = api.get_popularity_and_sex(name, start_year, end_year)
    if not data:
        data = [("No data available", "N/A", "N/A")]
    return render_template('search.html', name=name, data=data)

@app.route('/game_fail')
def game_fail():
    return render_template('game_fail.html')




if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port, debug=True)
