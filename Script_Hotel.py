from urllib.request import urlopen
from bs4 import BeautifulSoup
url = "https://www.tripadvisor.com/Hotels-g293758-Tunis_Tunis_Governorate-Hotels.html"
print("opening the first page")
try:
   page = urlopen(url)
except:
   print("Error opening the URL")
print("getting the list of hotels urls...")      
hotels_list=[]
first_page = BeautifulSoup(page, 'html.parser')
hotels_urls = first_page.findAll('a', {"class": "respListingPhoto"})
for i in hotels_urls:
      hotels_list.append(i['href'])
print(str(len(hotels_list))+" hotels are found in the first page");
urls_list=[]
pages_urls = first_page.findAll('a', {"class": "pageNum"})
print(str(len(pages_urls))+" other pages are found");
pages_counter=1

for url in pages_urls:        
    print("opening the page number:"+str(pages_counter))
    try:
       secondary_page = urlopen("https://www.tripadvisor.com"+url['href'])
    except:
       print("Error opening the URL")  
    print("the page number:"+str(pages_counter)+" is now open") 
    print("getting the list of hotels urls...")      
    page = BeautifulSoup(secondary_page, 'html.parser')
    hotels_urls = page.findAll('a', {"class": "respListingPhoto"})
    for i in hotels_urls:
          hotels_list.append(i['href'])
    pages_counter=pages_counter+1   
             
print("the total of hotels in Tunis is:"+str(len(hotels_list)))    

for hotel_url in hotels_list:
    print("opening hotel page")
    try:
       page = urlopen("https://www.tripadvisor.com"+hotel_url)
    except:
       print("Error opening the URL")
    print("getting the list of reviews from the first page...") 
    first_page = BeautifulSoup(page, 'html.parser')
    hotel_name=  first_page.find('h1', {"class": "hotels-hotel-review-atf-info-parts-Heading__heading--2ZOcD"}) 
    reviews = first_page.findAll('div', {"class": "hotels-community-tab-common-Card__card--ihfZB hotels-community-tab-common-Card__section--4r93H"})
    for review in reviews:    
        review_header = review.find('a',{"class":"location-review-review-list-parts-ReviewTitle__reviewTitleText--2tFRT"}).findAll('span')[1].getText()
        review_body = review.find('q',{"class":"location-review-review-list-parts-ExpandableReview__reviewText--gOmRC"}).findAll('span')[0].getText()
        #reviewer_city = reviews.find('span', {"class":"default social-member-common-MemberHometown__hometown--3kM9S small"}).findChildren()
        with open('scraped_text.csv', 'a') as file:
            file.write(hotel_name.getText()+",Tunis,"+review_header+","+review_body)
