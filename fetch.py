import psycopg2
import requests


def fetch_pokemones(id):
    api_url = f"https://pokeapi.co/api/v2/pokemon/{id}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        pokemon_name = data.get('name')
        pokemon_number = data.get("id")
        pokemon_type = data['types'][0]['type']['name']
        pokemon_img_front = data['sprites']['front_default']
        pokemon_img_back = data['sprites']['back_default']
        pokemon_mov_0 = data['moves'][0]['move']['name']
        if pokemon_number == 132:
            pokemon_mov_1 = 'None'
            pokemon_mov_2 = 'None'
            pokemon_mov_3 = 'None'
        else:
            pokemon_mov_1 = data['moves'][1]['move']['name']
            pokemon_mov_2 = data['moves'][2]['move']['name']
            pokemon_mov_3 = data['moves'][3]['move']['name']
        print(f"""Inserting: {pokemon_number}, {pokemon_name}, {pokemon_type}, {
              pokemon_mov_0}, {pokemon_mov_1}, {pokemon_mov_2}, {pokemon_mov_3}""")

        cursor.execute(
            "DELETE FROM pokemon WHERE number = %s",
            (pokemon_number,)
        )

        cursor.execute("""INSERT INTO pokemon (number, name, type, move_1, move_2, move_3, move_4) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                       (pokemon_number, pokemon_name, pokemon_type, pokemon_mov_0, pokemon_mov_1, pokemon_mov_2, pokemon_mov_3))
        cursor.execute("""UPDATE pokemon 
                        SET img_front = %s, img_back = %s 
                        WHERE number = %s
                        """, (pokemon_img_front, pokemon_img_back, pokemon_number))


conexion = psycopg2.connect(
    host="localhost",
    database="Pokemon_DB",
    user="postgres",
    password="password",
    port="5432",
)
cursor = conexion.cursor()

for i in range(1, 152):
    pokeid = i
    fetch_pokemones(pokeid)

conexion.commit()
cursor.close()
conexion.close()
