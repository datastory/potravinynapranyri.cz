import urllib2
from bs4 import BeautifulSoup
from googlemaps import GoogleMaps
import json
import re
f = open("potravinynapranyri.json", "w")
#api klic pro google maps
gmaps = GoogleMaps("YOU_GOOGLE_MAPS_API_KEY")
input = []

#zjisti pocet stranek
url = "http://www.potravinynapranyri.cz/Search.aspx?page=1"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page, from_encoding="utf-8")
lister = soup.find_all("a", class_="last")[0].get("href")

#najde jednotlive zaznamy
for y in range(1,int(lister.split("=")[1])):
	url = "http://www.potravinynapranyri.cz/Search.aspx?page=" + str(y)
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, from_encoding="utf-8")
	records_len = soup.find_all(id=re.compile("MainContent_rpDocList_lnkDocListControlledEntityName_"))

	#prohleda detaily kontrol
	for x in range(0,len(records_len)):
		link = soup.find_all(id=re.compile("MainContent_rpDocList_lbDocListSelect_"))[x].get("href")
		url_detail = "http://www.potravinynapranyri.cz/" + str(link)
		page_detail = urllib2.urlopen(url_detail)
		soup_detail = BeautifulSoup(page_detail, from_encoding="utf-8")

		#vytaha pozadovana data
		seller = soup_detail.find(id=re.compile("MainContent_lnkDocDetailControlledEntityName")).string.replace('"', "")
		product = soup_detail.find(id=re.compile("MainContent_lblDocDetailProductName")).string.replace('"', "")
		category = soup_detail.find(id=re.compile("MainContent_lnkDocDetailCategory")).string.replace('"', "")
		details = soup_detail.find(id=re.compile("MainContent_lblDocDetailLaboratoryBriefComment")).string.replace('"', "")
		address = soup_detail.find(id=re.compile("MainContent_lblDocDetailControlledEntityAddress")).string.encode("utf-8").replace('"', "")
		date = soup_detail.find(id=re.compile("MainContent_lblDocDetailSamplingDate")).string.replace('"', "")

		#zjisti souradnice podle adresy a nezjistene nahradi "null"
		try:
			lat, lng = gmaps.address_to_latlng(address)
		except:
			lat = "null"
			lng = "null"

		#naplni pole daty
		input.append({"product": product, "category": category, "date": date, "details": details, "seller": seller, "address": address, "lat": lat, "lng": lng})

#zapise JSON
f.write(json.dumps(input, sort_keys=True, indent=4))
f.close()