from django.shortcuts import render
from .marriott import email_marriott_results, fill_form, prepare_driver, scrape_results
from .models import Search
from guidez.settings import EMAIL_HOST_USER
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
import time

# def print_test(search_id):
#     search_id_int = int(search_id)
#     try:
#         searchobj = Search.objects.get(id=search_id_int)
#         if searchobj.recurrence > 0:
#             time.sleep(2)
#             print("print test")
#             searchobj.recurrence -= 1
#             searchobj.save()
#     except:
#         print("print_test function:::Search obj id=", search_id_int, " not found")

def search_and_email(searchobj_id):
    # try searching Marriott website
    res2 = []
    try:
        searchobj_id_int = int(searchobj_id)
        searchobj = Search.objects.get(pk=searchobj_id_int)
        if searchobj.recurrence < 1:
            try:
                DjangoJob.objects.get(name=searchobj_id).delete()
            except:
                return "reccurrence < 1, DjangoJob deletion failed"
    except:
        return "search_and_email: searchobj_id retrieve failed."
    try:
        print("prepare driver start")
        driver = prepare_driver("https://www.marriott.com/search/default.mi")
        fill_form(driver, searchobj.destination, searchobj.check_in, searchobj.check_out, searchobj.special_rates, searchobj.special_rates_code)
        time.sleep(1)
        print("scrape results start")
        res = scrape_results(driver)
        print("append results list")
        try:
            for i in range(len(res[0])):
                res2.append([res[0][i], res[3][i], res[2][i], res[1][i]])
                # this algorithm has an error if price is unavailable.
        except:
            print("Results append issue: some hotels may not have availability on selected dates")
        print("Search successfully completed")
    except:
        print("Search failed")
    # Try to email results
    try:
        if searchobj.recipient:
            email_marriott_results(res2, searchobj.recipient)
            print("Email results success")
    except:
        print("Email results failed")
    if not res2:
        return 'Results failed'
    if searchobj.recurrence > 0:
        searchobj.recurrence -= 1
        searchobj.save()
    return res2
