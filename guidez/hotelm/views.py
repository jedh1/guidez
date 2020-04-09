from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJob, register_job
from apscheduler.schedulers.background import BackgroundScheduler
import datetime, time
from .models import Search
from .forms import SearchForm, SignUpForm
from .marriott import email_marriott_results, fill_form, prepare_driver, scrape_results
from guidez.settings import EMAIL_HOST_USER
from .jobs import print_test

# Homepage
def index(request):
    return render(request, 'hotelm/index.html')

# About page
def about(request):
    time = datetime.datetime.now()
    searchobj = Search(
        recipient = 'test@test.com',
        destination = 'test',
        check_in = 'test check-in',
        check_out = 'test check-out',
        special_rates = 'test',
        recurrence = 5,
        )
    if request.user.is_authenticated:
        searchobj.user = request.user
    searchobj.save()
    searchobj_id=str(int(searchobj.id))
    scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)
    scheduler.add_job(print_test, 'interval', seconds = 3, id=searchobj_id, max_instances = 3, coalesce = True, args=[searchobj_id])
    register_job(scheduler)
    scheduler.start()
    print(scheduler.get_jobs())
    return render(request, 'hotelm/about.html', {'time': time})

# logout user page
def logout_request(request):
    logout(request)
    message = 'Logout successful.'
    return render(request, 'hotelm/index.html', {'message': message})

# login user page
def login_request(request):
    message = ''
    # if request.user.is_authenticated():
    #     return render(request, 'hotelm/index.html')
    if request.user.is_authenticated:
        return redirect('/', message = 'Already logged in')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            message = 'Login successful!'
            return redirect('/', message = 'Login successful!')
        else:
            form = AuthenticationForm()
            message = 'Invalid username or password.'
            return render(request, "auth/login.html", {"form": form, "message": message})
    else:
        form = AuthenticationForm()
        return render(request, "auth/login.html", {"form": form, "message": message})

# register user page
def register(request):
    if request.user.is_authenticated:
        return redirect('/', message = 'Already registered')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, 'hotelm/index.html', {'message': 'registered!'})
        else:
            form = SignUpForm()
            return render(request, 'auth/register.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'auth/register.html', {'form': form})

# Search page
def get_search(request):
    # If form is filled:
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # Create Search object
            searchobj = Search(
                recipient = form.cleaned_data['email'],
                destination = form.cleaned_data['destination'],
                check_in = form.cleaned_data['cin_date'],
                check_out = form.cleaned_data['cout_date'],
                special_rates = form.cleaned_data['special_rates'],
                special_rates_code = form.cleaned_data['special_rates_code']
            )
            if request.user.is_authenticated:
                searchobj.user = request.user
            if form.cleaned_data['email_box'] == True:
                searchobj.recurrence = 2
            searchobj.save()
            # try searching Marriott website
            try:
                print("prepare driver start")
                driver = prepare_driver("https://www.marriott.com/search/default.mi")
                fill_form(driver, searchobj.destination, searchobj.check_in, searchobj.check_out)
                time.sleep(1)
                print("scrape results start")
                res = scrape_results(driver)
                print("init results list")
                res2 = []
                print("append results list")
                for i in range(len(res[0])):
                    res2.append([res[0][i], res[3][i], res[2][i], res[1][i]])
                    # this algorithm has an error if price is unavailable.
                print("Search successfully completed")
            except:
                print("Search failed")
            # Try to email results
            try:
                email_marriott_results(res2, searchobj.recipient)
                print("Email results success")
            except:
                print("Email results failed")
            if searchobj.recurrence > 0:
                search_recurrence(searchobj.id)
            return render(request, 'hotelm/results.html', {'res': res2})
    # initial form screen
    else:
        form = SearchForm()
    return render(request, 'hotelm/search.html', {'form': form})

def history(request):
    items = Search.objects.all().filter(user=request.user)
    return render(request, 'hotelm/history.html', {'items': items})

def delete_search(request):
    if request.method == 'POST':
        search_id = int(request.POST.get('search_id'))
        search_obj = Search.objects.get(pk=search_id)
        search_obj.delete()
        search_id_str = str(search_id)
        try:
            DjangoJob.objects.get(name=search_id_str).delete()
            print("DjangoJob deleted. ID=",search_id)
        except:
            next
        items = Search.objects.all().filter(user=request.user)
        return render(request, 'hotelm/history.html', {'items': items})
