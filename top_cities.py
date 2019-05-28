#package used to grab the webpage
from urllib.request import urlopen as req

#package used to parse html
from bs4 import BeautifulSoup as soup

#packages to clean and reformat data
import regex

url = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"

#open connection
page = req(url)

#store raw html
page_raw = page.read()

#close connection
page.close()

#html parsing
page_soup = soup(page_raw, "html.parser")

#after inspecting the html file, "tr" tag contains the information we need
all_tables = page_soup.findAll("tr")

#creating the csv file
f_name = "top_cities.csv"
f = open(f_name, "w", encoding='utf-8-sig' )

#column headers
headers = "rank, city,city_desc, state\n"
f.write(headers)

#user input
print("Choose from the following options:")
print("1. Top 10 cities")
print("2. Whole list(5-10 minutes)")

while True:	
	user = input("Enter an option: ")
	if user.isnumeric() and user in str([1,2]):
		user = int(user)
		break

if user == 1:
	first = 20
	last = 30
else:
	first = 20
	last = 334

#looping for every rank
for table in all_tables[first:last]: #20:334

	#'td' tag holds the information of individual ranks
	hold = table.findAll('td')

	#extracting the rank
	position = hold[0].text.strip()

	#extracting the city
	city = hold[1].findAll('a')[0].text.strip()
	
	#extracting the state
	state = hold[2].text.strip()

	#extracting the city description from secondary page
	
	wiki = "https://en.wikipedia.org"
	#getting the city link
	city_url = wiki+table.a["href"]
	city_page = req(city_url)
	city_raw = city_page.read()
	city_page.close()
	city_soup = soup(city_raw, "html.parser")

	#'p' tag holds the required information
	city_hold = city_soup.findAll('p')

	#loop for extracting the text data
	for i in range(len(city_hold)):
		city_desc = city_hold[i].text.strip()
		#handling paranthesis
		city_desc = regex.subf(r"\((?:[^()]++|(?R))*+\)", "", city_desc)
		city_desc = regex.subf(r'\[(?:[^\]|]*\|)?([^\]|]*)\]', '', city_desc)
		#handling extra spaces
		city_desc = regex.subf(' +', ' ', city_desc)
		#handling commas
		city_desc = regex.subf(' ,+', ',', city_desc)
		#handling quotes
		city_desc = regex.subf('\"', '\'', city_desc)
		#handling slashes
		city_desc = regex.subf(r'/[^>]+?/', '', city_desc)
		#handling new line delimiter
		city_desc = regex.subf(r'[\n\r]+', '', city_desc)
		#to properly write the variable into csv
		city_desc = "\"" + city_desc + "\""
		if len(city_desc) > 75:
			break

	#writing each record into the csv file. replace is used just in case if there were any commas in between like in case of 'Washington, D.C.'
	f.write(position.replace(',','') + "," + city.replace(',','') + "," + city_desc + "," + state.replace(',','') + "\n")

#closing the file
f.close()
