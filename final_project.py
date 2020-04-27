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

    def __init__(self ,city = None, text = None,attraction = None):
        
        self.city = city #one
        self.text = text #one 
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
    def __init__(self ,category = None,  name = None, rating = None, review = None):
        self.category = category #five
        self.name = name #five
        self.rating = rating #five
        self.review = review #five
        #self.ranking = ranking #five
    
    #1. Alcatraz Island (Sights & Landmarks): 4.5 stars, 55.171 reviews
    def info(self):
        return self.name + " (" + self.category + "): " + str(self.rating)+ " stars, " + self.review 

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
    #print(resp)
    soup = BeautifulSoup(resp, 'html.parser')
    #print(soup)
    list_attractions = soup.find(class_ ="attractions-attraction-overview-pois-PoiGrid__wrapper--2H3Mo")  #there is only one
    clearfix = list_attractions.find_all("li", class_="attractions-attraction-overview-pois-PoiCard__item--3UzYK")
    #print(clearfix)
    i=0
    for attraction in clearfix:
        #print(f"attraction: {attraction}")
        if i < 5: 
            category = attraction.find(class_ = "_21qUqkJx").text.strip()
            #print(category)
            name = attraction.find("h3").text.strip()
            #print(name)
            rating1 = attraction.find(class_="ui_poi_review_rating")
            #print(rating1.find("span")["class"][1])
            rating = int(rating1.find("span")["class"][1][-2:])/10 
            #print(f"rating {rating}")
            #rating = attraction.find(class_= "ui_bubble_rating")['class'][1] #for value in element["class"] #class_= "ui_bubble_rating bubble_45"
            review = attraction.find(class_ ="reviewCount styleguide-bubble-rating-BubbleRatingWithReviewCount__reviewCount--37tMc").text.strip()
            #print(f"review {review}")
            attraction = Attraction(category,name, rating,review) #creating attraction instance, make sure order is correct
            #print(f"attraction{attraction}")
            lists.append(attraction) #list [attraction1,attraction2,attraction3,attraction4,attraction5]
            i = i+1
        else: 
            break
    #print(f"list{lists}")
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

def city_dict(list):

#1. search for city 
    BASEURL = "https://www.tripadvisor.com"
    city_dict={}
    #if bool(city_dict):
    #    pass
    #    print("there is a dictionary")
    #else:
    #    city_dict ={}
    for url in list:
        popular_cities = requests.get(url).text #json file
        soup = BeautifulSoup(popular_cities, 'html.parser')
        #print(type(soup))
        #print(f"soup:{soup}")
        city_sites = soup.find_all(class_= "mainName")  #list
        #print(f"city sites: {city_sites}")
        for pop_cities in city_sites:
            #print(pop_cities)
            city_dict[pop_cities.text.strip()]= BASEURL+pop_cities.find("a")["href"]
    #get_link = search_results.find(class_="ui_columns is-mobile result-content-columns") 
    #city_link = get_link["onclick"].split(",")[3]
    #city_info = requests.get(BASEURL + city_link) 
    #params = {"q": city} #city name (e.g: San Francisco) #what is my key? my value is San Francisco.
    #unique_key = construct_unique_key(BASEURL, params) #https://www.tripadvisor.com/Search?q=san%20francisco&searchSessionId=8F700871742D384F933251EC07147FFE1586551116577ssid&sid=E241DDA62B22634BF3C7848A0DFC22DA1586551117396&blockRedirect=true&rf=3
    #search = requests.get(BASEURL, params) #json file
    print(city_dict)
    return city_dict

def open_links(city_info_url):

#1. search for city 

    #BASEURL = "https://www.tripadvisor.com/Search"
    #params = {"q": city} #city name (e.g: San Francisco) #what is my key? my value is San Francisco.
    #unique_key = construct_unique_key(BASEURL, params) #https://www.tripadvisor.com/Search?q=san%20francisco&searchSessionId=8F700871742D384F933251EC07147FFE1586551116577ssid&sid=E241DDA62B22634BF3C7848A0DFC22DA1586551117396&blockRedirect=true&rf=3
    #search = requests.get(BASEURL, params) #json file

    #2. open city info

    #search = make_url_request_using_cache(BASEURL, params)

    #print(f"search: {search}")
    #soup = BeautifulSoup(search, 'html.parser')
    #print(type(soup))
    #print(f"soup:{soup}")
    #search_results = soup.find(class_= "search-results-list") 
    #print(f"search results: {search_results}")
    #get_link = search_results.find(class_="ui_columns is-mobile result-content-columns") 
    #city_link = get_link["onclick"].split(",")[3]

    #gets me to the next page
    BASEURL_2 = "http://tripadvisor.com"
    #city_info = requests.get(BASEURL_2 + city_link) 
    #city_info = make_url_request_using_cache(BASEURL_2+city_link)
    city_info = requests.get(city_info_url).text
    #print(city_info)
    soup = BeautifulSoup(city_info, 'html.parser')
    city1  = soup.find(class_ = "social-sections-GeoOverviewSection__header--zogLR") #one one class
    #print(city1)
    city = city1.find(class_="ui_header h2").text.strip() #only one under city #prints "Ann Arbor, Michigan"
    #print(f"City:{city}")
    text = soup.find(class_ = "cPQsENeY").text.strip()  #only one class
    #print(f"Text:{text}")

#3. open top attractions from city

    find_attraction = soup.find_all(class_="ui_link ui_header h2 ui_cluster_shelf_header_h2") # alist 
    attractions =[]
    for titles in find_attraction:
        #print(f"type: {type(titles)}")
        #print(titles.text.strip())
        if "Top attractions in" in titles.text.strip():
            try:
                #print(BASEURL_2 + titles["href"])
                attractions = get_instances_for_attraction(BASEURL_2 + titles["href"]) # a list of five attraction instances
                #print(f"Attractions 3 {attractions}")
            except:
                attractions = []
                print("no attractions")
    #print(attractions)
    city_all = City(city,text,attractions) #constructing a city instance
    #print(f"City_all: {city_all}")
    #print(City.about("Ann Arbor, Michigan"))
    
    #print(city_all.about())
    #print(city_all.city)
    #print(city_all.text)
    #print(city_all.attraction)
    #for attraction in city_all.attraction:
        #print(attraction.info())
        #print(type(attraction.category),attraction.category)
        #print(type(attraction.name), attraction.name)
        #print(type(attraction.rating),attraction.rating)
        #print(type(attraction.review), attraction.review)
    
    return city_all


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
    drop_attractions_sql = 'DROP TABLE IF EXISTS "Attraction"'
    
    create_city_sql ='''
        CREATE TABLE "City" (
            "CityName"  TEXT PRIMARY KEY UNIQUE,
            "Text"  TEXT NOT NULL
            )
    '''
    
    create_attractions_sql = '''
        CREATE TABLE 'Attraction'(
            'AttractionName' TEXT PRIMARY KEY UNIQUE,
            'Category' TEXT NOT NULL,
            'Rating' FLOAT NOT NULL,
            'Review' TEXT NOT NULL,
            'CityName' TEXT NOT NULL
        )
    '''
    cur.execute(drop_city_sql)
    cur.execute(drop_attractions_sql)
    cur.execute(create_city_sql)
    cur.execute(create_attractions_sql)
    conn.commit()
    conn.close()

def load_city(cities):#cities are city class instances
    conn = sqlite3.connect('trip_advisor.sqlite')
    cur = conn.cursor()
    insert_city = '''
        INSERT INTO City
        VALUES (?, ?)'''
    for city_info in cities: #objects from the city class
        cur.execute(insert_city, [city_info.city, city_info.text])
    conn.commit()

def load_attraction(cities):
    conn = sqlite3.connect('trip_advisor.sqlite')
    cur = conn.cursor() 
    insert_attraction = '''
        INSERT INTO Attraction
        VALUES (?,?,?,?,?)'''
    for city in cities: #objects from the city class
        city_name = city.city
        
        for attractions in city.attraction:
            category= attractions.category
            name = attractions.name
            rating = attractions.rating
            review = attractions.review
            cur.execute(insert_attraction, [name, category, rating, review, city_name])
    conn.commit()



#create_db()

    # put all the data in sql:  
    # select (*) from city where city = "Ann Arbor". If no result, info is not in database. Call request from code. 
    # write another function about Inserting. Call the function inside of the exisitng functions. 
    # write info into database before writing class. 

#city_dict = {"Paris":"https://www.tripadvisor.com/Tourism-g187147-Paris_Ile_de_France-Vacations.html", "Ann Arbor": 
#"https://www.tripadvisor.com/Tourism-g29556-Ann_Arbor_Michigan-Vacations.html", 
#"New York":"https://www.tripadvisor.com/Tourism-g60763-New_York_City_New_York-Vacations.html"}


if __name__ == "__main__":
    create_db()
    city_dict = city_dict(["https://www.tripadvisor.com/TravelersChoice-Destinations-cPopular-g191","https://www.tripadvisor.com/TravelersChoice-Destinations-cPopular-g1"])
    #city_dictionary = city_dict("https://www.tripadvisor.com/TravelersChoice-Destinations-cPopular-g191")
    print(city_dict.values())
    cities = []
    for url in city_dict.values():
        city_instances = open_links(url)
   #download data from multiple cities
        cities.append(city_instances)
    load_city(cities)
    load_attraction(cities)
