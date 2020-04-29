from django.shortcuts import render
from requests.compat import quote_plus  #Automatically add %20 in spaces in your search
from bs4 import BeautifulSoup
import requests
from . import models

# Create your views here.
def home(request):
    return render(request, 'base.html')


def search(request):
    if request.method == 'POST':
        BASE_JIJI_URL = 'https://jiji.ng/search?query={}'
        search = request.POST.get('search')
        models.Search.objects.create(search=search)
        final_url = BASE_JIJI_URL.format(quote_plus(search))

        #Getting the webpage, creating a Response object.
        response = requests.get(final_url)

        #Extracting the source code of the page
        data = response.text

        #Passing the source code to Beautiful Soup to create a BeautifulSoup object for it.
        soup = BeautifulSoup(data, features='html.parser')

        #Extracting all the <div> tags whose class name is 'b-list-advert__item' into a list

        post_listings = soup.find_all('div', {'class': 'b-list-advert__item'})

        final_postings = []
        for post in post_listings:
            post_title = post.find(class_='qa-advert-title').text
            post_url = post.find('a').get('href')

            if post.find(class_='b-list-advert__item-price'):
                post_price = post.find(class_='b-list-advert__item-price').text
            else:
                post_price = 'N/A'


            if post.find(class_='b-list-advert__item-image'):
                post_image_src = post.findAll('img')
                string_src = str(post_image_src)
                post_image_url = string_src.split(" ")[-1].split('=')[-1].split('"')[1]
            else:
                post_image_url = 'https://losangeles.craigslist.org/images/peace.jpg'

            final_postings.append((post_title, post_url, post_price, post_image_url))

        context = {'search': search,
                   'final_postings': final_postings,
                   "final_url": final_url
                   }

        return render(request, 'jiji_app/search.html', context)
    return render(request, 'jiji_app/search.html')