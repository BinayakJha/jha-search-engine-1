from unittest import result
from django.http import HttpResponse, request
from django.shortcuts import render
import requests
from requests_html import HTMLSession
import urllib
import replit
import random
# Create your views here.

# ------------------------------------------------------------------------------------
# Get the source from the url function
# ------------------------------------------------------------------------------------

def get_source(url):
    user_agent_list = [
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Linux x86_64; Mail.RU_Bot/Fast/2.0; +http://go.mail.ru/help/robots)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 BingPreview/1.0b',
    ]
    try:
        headers ={"User-Agent": user_agent_list[random.randint(0, len(user_agent_list)-1)]}
        print('User agent ', headers)

        session = HTMLSession()
        response = session.get(url, headers=headers)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

# ------------------------------------------------------------------------------------
# Scraping Google Search
# ------------------------------------------------------------------------------------

def scrape_google(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.',
                      'https://google.',
                      'https://webcache.googleusercontent.',
                      'http://webcache.googleusercontent.',
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)
    return links

# ------------------------------------------------------------------------------------
# getting results from the search
# ------------------------------------------------------------------------------------

def get_results(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query+"&source=hp&start=0"+"&num=100")
    # replace whitespace with +
    query = query.replace(" ", "+")
    return response

# brave results 

def brave_results(query):
    query = urllib.parse.quote_plus(query)
    response2 = get_source("https://search.brave.com/search?q=" + query)
    # replace whitespace with +
    query = query.replace(" ", "+")
    return response2

# ------------------------------------------------------------------------------------
# brave search
# ------------------------------------------------------------------------------------
def brave_search(response2):
    output2 = []
    results2 = response2.html.find('#side-right')
    for result2 in results2:
        data2 = dict()
        try:

            data2['title1'] = result2.find('.infobox-title', first=True).text
            data2['description'] = result2.find('.infobox-description', first=True).text
            data2['big_description'] = result2.find('.body .mb-6', first=True).text
            data2['big_description'] = data2['big_description'].replace("Wikipedia", "")
            data2['links'] = result2.find('.links a', first=True).attrs['href']
        except:
            pass
        
        try:
            data2['rating_text'] = result2.find('.r-num')[1].text
            data2['website_url']= result2.find('#website_url a', first=True).attrs['href']
        except:
            pass
        try:
            data2['rating_text_0'] = result2.find('.r-num')[0].text
        except:
            pass
        try:
            # take all the html too
            data2['code'] = result2.find('.infobox-attr pre ', first=True).html
            data2['code_text'] = result2.find('.infobox-attr p', first=True).html
            print(data2['code_text'])
        except:
            pass
         # wikipedia image scraping
        try:
            # image
            img_url = data2['links']

            try:
                session = HTMLSession()
                response3 = session.get(img_url)

            except requests.exceptions.RequestException as e:
                print(e)
            try:
                data2['image_url'] = response3.html.find('.infobox-image img')[0].attrs['src']
            except:
                data2['image_url'] = response3.html.find('.thumbinner img')[0].attrs['src']
        except:
            pass
       
        output2.append(data2)
    return output2
# ------------------------------------------------------------------------------------
# brave search function
# ------------------------------------------------------------------------------------
def search_1(query):
    response2 = brave_results(query)
    return brave_search(response2)


# ------------------------------------------------------------------------------------
# parsing results
# ------------------------------------------------------------------------------------

def parse_results(response):
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = ".yuRUbf h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"
    css_identifier_cite = ".iUh30"
    # related search tab
    css_identifier_featured = ".GyAeWb"
    results = response.html.find(css_identifier_result)
    # related search tab

    output = []
    for result in results:
        data = {}
        try:
            data['title'] = result.find(css_identifier_title, first=True).text
            data['link'] = result.find(css_identifier_link, first=True).attrs['href']
            data['favicon'] = "https://www.google.com/s2/favicons?sz=64&domain_url=" + data['link']
            data['text'] = result.find(css_identifier_text, first=True).text
            # data['text2'] = data['text'].replace("\n", "")
            # filter the links from the text
            data['text'] = data['text'].replace(data['link'], '')
            # cite functions
            data['cite'] = result.find(css_identifier_cite, first=True).text
            data['cite'] = data['cite'].replace("...", "")
            data['cite'] = data['cite'].replace("›", "")
        except:
            pass
        # close cite functions
        # youtube video image url
        if "/watch?v" in data['link']:
            link3 = data['link'][32:]
            data['yt_url'] = f"https://i.ytimg.com/vi/{link3}/0.jpg"
        output.append(data)
    # data['featured_answer'] = people_also_ask.get_simple_answer('2+2')
    return output


# ------------------------------------------------------------------------------------
# doing google search
# ------------------------------------------------------------------------------------

def google_search(query):
    response = get_results(query)
    return parse_results(response)

# ------------------------------------------------------------------------------------
# home function
# ------------------------------------------------------------------------------------

def home(request):
    return render(request, 'core/home.html')

# ------------------------------------------------------------------------------------
# google sidesearch
# ------------------------------------------------------------------------------------

# def side_search(response):
    # output2 = []
    # # try:
    # results2 = response.html.find('.liYKde')
    # # except:
    # for result2 in results2:
    #     data2 = {}
    #     try:
    #         data2['title1'] = result2.find('.qrShPb', first=True).text
    #     except:
    #         pass
    #     try:
    #         data2['description'] = result2.find('.wwUB2c', first=True).text
    #     except:
    #         pass
    #     try:
    #         data2['big_description'] = result2.find('.kno-rdesc', first=True).text
    #         data2['big_description'] = data2['big_description'].replace("Description", "")
    #         data2['big_description'] = data2['big_description'].replace("Wikipedia", "")

    #     except:
    #         pass
    #     try:
    #         data2['links'] = result2.find('.ruhjFe', first=True).attrs['href']
    #     except:
    #         pass
    #     # try:
    #     #     data2['rating'] = result2.find('.h6', first=True).text
    #     #     data2['rating_image'] = result2.find('.rating-source', first=True).attrs['src']
    #     #     data2['rating_text'] = result2.find('.r .flex-hcenter .text-sm', first=True).text
    #     # except:
    #     #     pass
    #      # wikipedia image scraping
    #     try:
    #         # image
    #         img_url = data2['links']

    #         try:
    #             session = HTMLSession()
    #             response3 = session.get(img_url)

    #         except requests.exceptions.RequestException as e:
    #             print(e)
    #         try:
    #             data2['image_url'] = response3.html.find('.infobox-image img')[0].attrs['src']
    #         except:
    #             data2['image_url'] = response3.html.find('.thumbinner img')[0].attrs['src']
    #     except:
    #         pass
    #     output2.append(data2)

    # return output2

# ------------------------------------------------------------------------------------
# brave search function
# ------------------------------------------------------------------------------------

def search_1(query):
    response2 = brave_results(query)
    return brave_search(response2)

# ------------------------------------------------------------------------------------
# main search function
# ------------------------------------------------------------------------------------

def search(request):
    results = None
    brave__results = None
    if 'query' in request.GET:
        # Fetch search data
        query= request.GET['query']
        results= google_search(query)

        # Fetch brave data
        brave__results = search_1(query)
        if brave__results == [{}]:
            brave__results = None
    return render(request, 'core/search.html', {'data': results, 'data2':brave__results})

def get_results_2(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://depositphotos.com/stock-photos/" + query+".html")
    # replace whitespace with +
    query = query.replace(" ", "-")
    return response
# ------------------------------------------------------------------------------------
#  image search function
# ------------------------------------------------------------------------------------
def scrape_images(response):
    images_lis =response.html.find('.flex-files')
    output = []
    for image in images_lis:
        data = {}
        for i in range(1, 30):
            data['image'] = image.find('img')[i].attrs['src']
            output.append(data)
            i += 1
    return output

def image_search(query):
    response = get_results_2(query)
    return image_search(response)

# ------------------------------------------------------------------------------------
# image search function
# ------------------------------------------------------------------------------------
def image_search(request):
    results = None
    if 'query' in request.GET:
        # Fetch search data
        query= request.GET['query']
        results= image_search(query)
    return render(request, 'core/image_search.html', {'data': results})