from bs4 import BeautifulSoup
import requests
import json
import sqlite3
CACHE_FILENAME = "cache.json"


class City:
    '''a city, description text and attractions
    Instance Attributes
    -------------------
    text: string
        description of the city 
    city: string
        city and state/country of the attraction (e.g. 'San Francisco, California or Taipei, Taiwan')
    attraction: 
        the city's top 5 attractions and details
    '''

    def __init__(self , text = None, city = None, attraction = None):
        
        self.text = text #one 
        self.city = city #one
        self.attraction = attraction #one list of the five attractions
    
    # San Francisco: Every neighborhood in San Francisco has its own personality, 
    # from the hippie chic of the Upper Haight to the hipster grit of the Mission...
    def about(self):
        return self.city + ": " + self.text

class Attraction: #consruct first and add to list. then construct the city. 
    '''a city's top 5 attractions and details
    Instance Attributes
    -------------------
    name: string
        the attraction ranking and name of atraction(e.g. '1. Alcatraz Island')
    category: string
        the category of an attraction (e.g. 'Sights & Landmarks')
    rating: string
        the average rating of the attraction (e.g. '4.5')
    review: string
        number of reviews the attraction has(e.g. '555 reviews')
    '''
    def __init__(self , name = None, category = None, rating = None, review = None):
        self.category = category #five
        self.name = name #five
        self.rating = rating #five
        self.review = review #five
        #self.ranking = ranking #five
    
    #1. Alcatraz Island (Sights & Landmarks): 4.5 stars, 55.171 reviews
    def info(self):
        return self.name + " (" + self.category + "): " + self.rating+ " stars, " + self.review 

#part 2
"""def get_city_text_instance(site_url,attraction):
    '''Make an instances from a city information url.
    
    Parameters
    ----------
    site_url: string
        The URL for a city information url in trip advisor.
    
    Returns
    -------
    instance
        a list of five attraction instances
    '''
    #BASE_URL = site_url 
    #resp = make_url_request_using_cache(site_url)
    #soup = BeautifulSoup(resp,'html.parser')
    
    city1  = soup.find(class_ = "social-sections-GeoOverviewSection__header--zogLR") #one one class
    city = city1.find(class_="ui_header h2").text.strip() #only one under city #prints "Ann Arbor, Michigan" == $0 <!-- -->
    text = soup.find(class_ = "cPQsENeY").text.strip()  #only one class

    print(city)
    print(text)
    city_info= City(city, text,attraction)
    return city_info"""


def get_instances_for_attraction(attraction_url):
    '''Make a list of five attraction instances from a city attractions URL.
    
    Parameters
    ----------
    state_url: string
        The URL for a city attractions page in trip advisor
    
    Returns
    -------
    list
        a list of five attraction instances
    '''
    lists = []
    resp = make_url_request_using_cache(attraction_url)
    soup = BeautifulSoup(resp, 'html.parser')
    list_attractions = soup.find(class_ ="attractions-attraction-overview-pois-PoiGrid__wrapper--2H3Mo")  #there is only one
    clearfix = list_attractions.find_all("li", class_="attractions-attraction-overview-pois-PoiCard__item--3UzYK")
    #print(clearfix)
    i=0
    for attraction in clearfix:
        if i > 5: 
            category = attraction.find(class_ = "_21qUqkJx").text.strip()
            name = attraction.find("h3") 
            rating1 = attraction.find(class_="ui_poi_review_rating  ")
            rating = int(rating1.find("span")["class"][-3:])/10 
            #rating = attraction.find(class_= "ui_bubble_rating")['class'][1] #for value in element["class"] #class_= "ui_bubble_rating bubble_45"
            review = attraction.find(class_ ="reviewCount styleguide-bubble-rating-BubbleRatingWithReviewCount__reviewCount--37tMc").text.strip()
            attraction = Attraction(name,category,rating,review) #creating attraction instance, make sure order is correct
            lists.append(attraction) #list [attraction1,attraction2,attraction3,attraction4,attraction5]
            i = i+1
        else: 
            break

    return lists # five attraction instances all in a list

#make and save cache
def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read() #json strings
        cache_dict = json.loads(cache_contents) #json into dictionary
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict) #python into json string
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def open_links(city):

#1. search for city 

    BASEURL = "https://www.tripadvisor.com/Search"
    params = {"q": city} #city name (e.g: San Francisco) #what is my key? my value is San Francisco.
    unique_key = construct_unique_key(BASEURL, params) #https://www.tripadvisor.com/Search?q=san%20francisco&searchSessionId=8F700871742D384F933251EC07147FFE1586551116577ssid&sid=E241DDA62B22634BF3C7848A0DFC22DA1586551117396&blockRedirect=true&rf=3
    #search = requests.get(BASEURL, params) #json file

    #2. open city info

    search = make_url_request_using_cache(BASEURL, params)
    soup = BeautifulSoup(search, 'html.parser')
    search_results = soup.find(class_= "search-results-list") 
    get_link = search_results.find(class_="ui_columns is-mobile result-content-columns") 
    city_link = get_link["onclick"].split(",")[3]

    #gets me to the next page
    BASEURL_2 = "http://tripadvisor.com"
    #city_info = requests.get(BASEURL_2 + city_link) 
    city_info = make_url_request_using_cache(BASEURL_2+city_link)
    soup = BeautifulSoup(city_info, 'html.parser')
    city1  = soup.find(class_ = "social-sections-GeoOverviewSection__header--zogLR") #one one class
    city = city1.find(class_="ui_header h2").text.strip() #only one under city #prints "Ann Arbor, Michigan" == $0 <!-- -->
    text = soup.find(class_ = "cPQsENeY").text.strip()  #only one class

#3. open top attractions from city

    find_attraction = soup.find(class_="ui_link ui_header h2 ui_cluster_shelf_header_h2")
    for titles in find_attraction:
        if "Top Attractions in" in titles.text.strip():
            try:
                attractions = get_instances_for_attraction(BASEURL_2 + titles["href"]) # a list of five attraction instances
            except:
                attractions = []
    
    city = City(city,text,attractions) #constructing a city instance

"""
city.about()

    for attraction in city.attraction:
        print(attraction.info())
"""



def construct_unique_key(baseurl, params): # key for cache
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}') #key_value
    param_strings.sort() #alphabetical order
    unique_key = baseurl + connector + connector.join(param_strings) #list into a string
    return unique_key

def make_url_request_using_cache(url,params={}):
    ''' fetches the data using the url and params provided

    Parameters
    ----------
    url: string
        The URL of the site
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        data in a dictionary
    '''
    cache_dict  = open_cache()
    request_key = construct_unique_key(url, params) #request key is an url
    #result = {}
    if request_key in cache_dict: 
        # a cache exists 
        print("Using cache")
        result = cache_dict[request_key]
    else: 
        # a cache doesn't exist
        print("Fetching")
        try:
            result = requests.get(url, params).text #json() or text 
            cache_dict[request_key] = result
            save_cache(cache_dict)
        except:
            print("error when reading from url")
            result ={}
    return result #text

    #lst[:4] For ele in lst: ele.find(div=, class_=) 


    # create tables and columns
    # city table: City and text, state
    # attraction table: ID(autoincrement), attraction name, rating, reviews, category, City (foreign key)

def create_db():
    conn = sqlite3.connect('trip_advisor.sqlite')
    cur = conn.cursor()

    drop_city_sql = 'DROP TABLE IF EXISTS "City"'
    drop_attractions_sql = 'DROP TABLE IF EXISTS "Attractions"'
    
    create_city_sql ='''
        CREATE TABLE "City" (
            "CityName"  TEXT PRIMARY KEY UNIQUE,
            "CityInfo"  TEXT NOT NULL
            )
    '''
    
    create_attractions_sql = '''
        CREATE TABLE 'Attractions'(
            'AttractionName' TEXT PRIMARY KEY UNIQUE,
            'Category' TEXT NOT NULL,
            'Rating' INTEGRER NOT NULL,
            'CityName' TEXT NOT NULL
        )
    '''
    cur.execute(drop_city_sql)
    cur.execute(drop_attractions_sql)
    cur.execute(create_city_sql)
    cur.execute(create_attractions_sql)
    conn.commit()
    conn.close()

create_db()

    # put all the data in sql:  
    # select (*) from city where city = "Ann Arbor". If no result, info is not in database. Call request from code. 
    # write another function about Inserting. Call the function inside of the exisitng functions. 
    # write info into database before writing class. 

    