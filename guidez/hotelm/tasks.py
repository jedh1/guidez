from background_task import background
from django.shortcuts import render
from .marriott import email_marriott_results, fill_form, prepare_driver, scrape_results
from .models import Search
from guidez.settings import EMAIL_HOST_USER
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

@background(schedule=1)
def email_test():
    print('email_test start')
    email_marriott_results(['test1','test2','test3','test4'], 'jedhcl@gmail.com')

@background(schedule=10)
def search_recurrence(search_id):
    searchobj = Search.objects.get(pk=search_id)
    if searchobj.recurrence == 0:
        print("object recurrence == 0")
        return
    searchobj.recurrence -= 1
    searchobj.save()
    print("obj.recurrence value after run:", searchobj.recurrence)
    try:
        print("Recurrence search, prepare driver start")
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
        print("Search: successfully completed")
    except:
        print("Search: failed")
    # Try to email results
    try:
        email_marriott_results(res2, searchobj.recipient)
        print("Email results: success")
    except:
        print("Email results: failed")
    if searchobj.recurrence > 0:
        search_recurrence(searchobj.id)
    return print('search_recurrence successful')
