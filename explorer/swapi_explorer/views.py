import hashlib
import os

import petl as etl
import requests as req
from django.shortcuts import render
from django.views import View

from explorer.settings import MEDIA_ROOT

from .models import DataSet

# Create your views here.


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


class Home(View):
    template_name = 'home.html'
    http_method_names = ['get', 'post']
    planets = {}

    def parse_character(self, character):
        character = {key: value for key, value in character.items() if key in CHARACTER_FIELDS}
        character['date'] = character['edited'][:10]
        del character['edited']
        character['homeworld'] = self.planets.get(character['homeworld'], 'N/A')
        return character

    def get(self, request):
        data_sets = DataSet.objects.all().order_by('-pk')
        return render(request, self.template_name, {'data_sets': data_sets})

    def post(self, request):
        _next = 'https://swapi.co/api/people'
        _next_planets = 'https://swapi.co/api/planets'
        planets = []
        characters = []
        while _next is not None:
            resp = req.get(_next).json()
            _next = resp['next']
            characters.extend(resp['results'])
        while _next_planets is not None:
            resp = req.get(_next_planets).json()
            _next_planets = resp['next']
            planets.extend(resp['results'])
        self.planets = {planet['url']: planet['name'] for planet in planets}
        characters = [self.parse_character(character) for character in characters]
        filename = hashlib.md5().hexdigest() + '.csv'
        table = etl.fromdicts(characters)
        etl.tocsv(table, os.path.join(MEDIA_ROOT, filename))
        DataSet.objects.create(filename=filename)
        data_sets = DataSet.objects.all().order_by('-pk')
        return render(request, self.template_name, {'data_sets': data_sets})


class SingleSet(View):
    template_name = 'characters.html'

    def get(self, request, filename):
        table = etl.fromcsv(os.path.join(MEDIA_ROOT, filename))
        characters = etl.listoftuples(table)
        return render(request, self.template_name, {'headers': characters[0],
                                                    'characters': characters[1:]})
