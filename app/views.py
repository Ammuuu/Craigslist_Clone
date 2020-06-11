import requests
from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGSLIST_URL = "https://losangeles.craigslist.org/search/bbb?query={}"
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


# Create your views here.
def home(request):
    return render(request, 'index.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    main_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(main_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://image.freepik.com/free-vector/beautiful-gold-star-background-arranged' \
                             '-decorating-various-celebrations_41084-382.jpg '

        final_postings.append((post_title, post_url, post_image_url))

    if not final_postings:
        search = "No Results Found"

    return_to_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'app/newSearch.html', return_to_frontend)
