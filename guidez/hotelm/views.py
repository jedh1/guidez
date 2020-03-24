from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime, time
from .models import Search
from .forms import SearchForm
from .marriott import prepare_driver, fill_form, scrape_results

# Create your views here.
def index(request):
    res1 = [['name1', 'location1', 'price1'], ['name2', 'location2', 'price2']]
    return render(request, 'hotelm/index.html', {'res': res1})

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
            try:
                print("prepare driver start")
                driver = prepare_driver("https://www.marriott.com/search/default.mi")
                fill_form(driver, searchobj.destination, searchobj.check_in, searchobj.check_out)
                time.sleep(1)
                print("scrape results start")
                res = scrape_results(driver)
                res2 = []
                for i in range(len(res[0])):
                    res2.append([res[0][i], res[1][i], res[2][i], res[3][i]])
                print("Search successfully completed")
            except:
                print("Search failed")
            return render(request, 'hotelm/results.html', {'res': res2})
    else:
        form = SearchForm()
    return render(request, 'hotelm/search.html', {'form': form})
