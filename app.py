from flask import Flask, request, render_template, redirect
import psycopg2
from psycopg2.extras import RealDictCursor
app = Flask(__name__)


def get_db_connection():
    # Configura aquí tus credenciales y parámetros de conexión a la base de datos
    conn = psycopg2.connect(
        dbname='Pokemon_DB',
        user='postgres',
        password='password',
        host='localhost',
        port='5432'
    )
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pokemon')
def pokemon():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM pokemon;')
    pokemons = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('pokemon.html', pokemons=pokemons)


@app.route('/trainers', methods=['GET', 'POST'])
def trainers():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        new_trainer_name = request.form['trainer_name']
        cur.execute('SELECT COALESCE(MAX(id), 0) + 1 FROM trainers;')
        new_id = cur.fetchone()[0]
        cur.execute('INSERT INTO trainers (id, name) VALUES (%s, %s);',
                    (new_id, new_trainer_name))
        conn.commit()

    cur.execute('SELECT * FROM trainers;')
    trainers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('trainers.html', trainers=trainers)


@app.route('/teams', methods=['GET', 'POST'])
def teams():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        team_name = request.form['team_name']
        trainer_id = int(request.form['trainer'])
        pokemon1_id = int(request.form['pokemon1'])
        pokemon2_id = int(request.form['pokemon2'])
        pokemon3_id = int(request.form['pokemon3'])

        # Get the next ID for the new team
        cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM teams")
        new_id = cur.fetchone()[0]

        # Insert new team
        cur.execute(
            "INSERT INTO teams (id, team_name, trainer_id, pokemon1_id, pokemon2_id, pokemon3_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (new_id, team_name, trainer_id, pokemon1_id, pokemon2_id, pokemon3_id)
        )
        conn.commit()

        cur.close()
        conn.close()
        return redirect('/teams')

    # Fetch teams and other data for GET request
    cur.execute("SELECT teams.id, teams.team_name, trainers.name, pokemon1.name, pokemon2.name, pokemon3.name "
                "FROM teams "
                "JOIN trainers ON teams.trainer_id = trainers.id "
                "JOIN pokemon AS pokemon1 ON teams.pokemon1_id = pokemon1.number "
                "JOIN pokemon AS pokemon2 ON teams.pokemon2_id = pokemon2.number "
                "JOIN pokemon AS pokemon3 ON teams.pokemon3_id = pokemon3.number")
    teams = cur.fetchall()

    cur.execute("SELECT id, name FROM trainers")
    trainers = cur.fetchall()

    cur.execute("SELECT number, name FROM pokemon")
    pokemon_list = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('teams.html', teams=teams, trainers=trainers, pokemon_list=pokemon_list)


@app.route('/battles', methods=['GET', 'POST'])
def battles():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        team1_id = int(request.form['team1'])
        team2_id = int(request.form['team2'])
        city = request.form['city']
        date = request.form['date']
        winner_id = int(request.form['winner'])

        # Get the next ID for the new battle
        cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM battles")
        new_id = cur.fetchone()[0]

        # Insert new battle
        cur.execute(
            "INSERT INTO battles (id, team1_id, team2_id, city, date, winner_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (new_id, team1_id, team2_id, city, date, winner_id)
        )
        conn.commit()

        cur.close()
        conn.close()
        return redirect('/battles')

    # Fetch battles and other data for GET request
    cur.execute("SELECT battles.id, team1.team_name AS team1_name, team2.team_name AS team2_name, battles.date, battles.city, battles.winner_id "
                "FROM battles "
                "JOIN teams AS team1 ON battles.team1_id = team1.id "
                "JOIN teams AS team2 ON battles.team2_id = team2.id")
    battles = cur.fetchall()

    cur.execute("SELECT id, team_name FROM teams")
    teams = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('battles.html', battles=battles, teams=teams)


if __name__ == '__main__':
    app.run(debug=True)
