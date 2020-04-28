import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from django.utils import timezone
from . models import Search
from django.http import HttpResponseRedirect

BASE_CGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'
# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    if search:
        time = timezone.now()
        s1=Search.objects.create(search=search,created=time)
    
    final_url = BASE_CGSLIST_URL.format(quote_plus(search))
    no_res = ''
    
    try:
        response = requests.get(final_url)
        data = response.text
        soup =BeautifulSoup(data, features='html.parser')

        post_listings = soup.find_all('li', {'class': 'result-row'})
        
        if soup.find_all('div', {'class': 'alert alert-sm alert-warning'}):
            no_result = soup.find_all('div', {'class': 'alert alert-sm alert-warning'})    
            no_res = "No result found For '{}' search. (All words must match)".format(search)
            print(no_result, ' ', no_res)

        final_postings = []

        for post in post_listings:
            post_titles = post.find(class_='result-title').text
            post_url = post.find('a').get('href')
            
            if post.find(class_='result-price'):
                post_price = post.find(class_='result-price').text
            else:
                post_price = 'N/A'

            if post.find(class_='result-image').get('data-ids'):
                post_image = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
                post_image_url = BASE_IMAGE_URL.format(post_image)
            else:
                post_image_url = 'https://previews.123rf.com/images/urfandadashov/urfandadashov1809/urfandadashov180901275/109135379-photo-not-available-vector-icon-isolated-on-transparent-background-photo-not-available-logo-concept.jpg'
                print(post_image_url)

            final_postings.append((post_titles, post_url, post_price, post_image_url))
        

        stuff_for_front_end = {
            'search' : search,
            'final_postings': final_postings,
            'no_res' :no_res,
        }
    except:
        stuff_for_front_end = { 'errormessage' : 'Check Your Internet Connection'}
    if search:
        s1.save()
    return render(request, 'my_app/new_search.html', stuff_for_front_end)

def search_history(request):
    data = Search.objects.all().order_by('-created')
    stuff_for_front_end = {
        'history' : data,
    }
    return render(request, 'my_app/search_history.html',stuff_for_front_end)

def delete_history(request, history_id):
    Search.objects.get(id=history_id).delete()
    return HttpResponseRedirect('/')

def delete_all_history(request):
    Search.objects.all().delete()
    return HttpResponseRedirect('/')