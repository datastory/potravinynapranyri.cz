import urllib2
from bs4 import BeautifulSoup
import re
#vysledky se ulozi do souboru .csv (hodnoty oddelene carkami)
f = open("potraviny.csv", "w")

# zjisti pocet stranek ve strankovani
url = "http://www.potravinynapranyri.cz/Search.aspx?page=1"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page, from_encoding="utf-8")
lister = soup.find_all("a", class_="last")[0].get("href")


#projde vsechny stranky a nalezne v nich odkazy na detaily jednotlivych potravin
for y in range(1,int(lister.split("=")[1])):
	url = "http://www.potravinynapranyri.cz/Search.aspx?page=" + str(y)
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, from_encoding="utf-8")
	records_len = soup.find_all(id=re.compile("MainContent_rpDocList_lnkDocListControlledEntityName_"))

    #projde vsechny detaily potravit, vytaha z nich pozadovane udaje a ulozi do souboru
	for x in range(0,len(records_len)):
		link = soup.find_all(id=re.compile("MainContent_rpDocList_lbDocListSelect_"))[x].get("href")
		url_detail = "http://www.potravinynapranyri.cz/" + str(link)
		page_detail = urllib2.urlopen(url_detail)
		soup_detail = BeautifulSoup(page_detail, from_encoding="utf-8")

		producer = soup_detail.find(id=re.compile("MainContent_lnkDocDetailControlledEntityName")).string
		product = soup_detail.find(id=re.compile("MainContent_lblDocDetailProductName")).string
		category = soup_detail.find(id=re.compile("MainContent_lnkDocDetailCategory")).string
		details = soup_detail.find(id=re.compile("MainContent_lblDocDetailLaboratoryBriefComment")).string
		address = soup_detail.find(id=re.compile("MainContent_lblDocDetailControlledEntityAddress")).string

		f.write (product.encode("utf-8") + "," + category.encode("utf-8") + "," + details.encode("utf-8") + "," + producer.encode("utf-8") + "," + address.encode("utf-8") + "\n")
		print("Zapisuji " + str(x + 1) + ". zaznam.")


f.close()