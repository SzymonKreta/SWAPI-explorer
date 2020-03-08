import os
import hashlib

from django.views import View
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render

import requests as req
import petl as etl

from .models import DataSet
from .utils import parse_character
from explorer.settings import MEDIA_ROOT
# Create your views here.

class Home(View):
    template_name = 'home.html'
    http_method_names = ['get', 'post']

    def get(self, request):
        data_sets = DataSet.objects.all().order_by('-pk')
        return render(request, self.template_name, {'data_sets': data_sets})

    def post(self, request):
        _next = 'https://swapi.co/api/people'
        characters = []
        while _next is not None:
            resp = req.get(_next).json()
            _next = resp['next']
            characters.extend(resp['results'])
        characters = [parse_character(character) for character in characters]
        filename = hashlib.md5().hexdigest() + '.csv'
        DataSet.objects.create(filename=filename)
        table = etl.fromdicts(characters)
        etl.tocsv(table, os.path.join(MEDIA_ROOT, filename))
        data_sets = DataSet.objects.all()
        return render(request, self.template_name, {'data_sets': data_sets})


class SingleSet(View):
    template_name = 'characters.html'

    def get(self, request, filename):
        table = etl.fromcsv(os.path.join(MEDIA_ROOT, filename))
        characters = etl.listoftuples(table)
        return render(request, self.template_name, {'headers': characters[0],
                                                    'characters': characters[1:]})

