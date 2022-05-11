from django.shortcuts import render, get_object_or_404, redirect
import requests

from .models import City
from .forms import CityForm


def index(request):
    appid = '1261b7e0b24809cf25a2a41921e01582'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='+appid

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []
    for city in cities:
        new_url = url.format(city.name).replace(' ', '%20')
        res = requests.get(new_url).json()
        city_info = {
            'city': city.name,
            'temp': res["main"]["temp"],
            'icon': res["weather"][0]["icon"],
            'pk': city.pk
        }
        all_cities.append(city_info)
    contex = {'all_info': all_cities, 'form': form}
    return render(request, 'weather/index.html', contex)


def delete_city(request, pk):
    city = get_object_or_404(City, pk=pk)
    city.delete()
    return redirect('home')