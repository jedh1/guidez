from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime
from .models import Search
from .forms import SearchForm

# Create your views here.
def index(request):
    return render(request, 'hotelm/index.html')

def about(request):
    time = datetime.datetime.now()
    return render(request, 'hotelm/about.html', {'time': time})

def get_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            searchobj = Search(
                destination = form.cleaned_data['destination'],
                check_in = form.cleaned_data['cin_date'],
                check_out = form.cleaned_data['cout_date'],
                special_rates = form.cleaned_data['special_rates'],
                special_rates_code = form.cleaned_data['special_rates_code']
            )
            searchobj.save()
            Search.objects.all()
            return render(request, 'hotelm/search.html', {'form': form})
    else:
        form = SearchForm()
    return render(request, 'hotelm/search.html', {'form': form})
