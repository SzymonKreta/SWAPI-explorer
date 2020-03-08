import requests

CHARACTER_FIELDS = ['name',
                    'height',
                    'mass',
                    'hair_color',
                    'skin_color',
                    'eye_color',
                    'birth_year',
                    'gender',
                    'homeworld',
                    'edited']

def parse_character(character):
    character = {key: value for key, value in character.items() if key in CHARACTER_FIELDS}
    character['date'] = character['edited'][:10]
    del character['edited']
    character['homeworld'] = requests.get(character['homeworld']).json()['name']
    return character