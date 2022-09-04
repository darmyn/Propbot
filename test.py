from bs4 import BeautifulSoup
import requests

url = "https://www.youtube.com/watch?v=Iuk1znROeKg"
result = requests.get(url).text
doc = BeautifulSoup(result, "html.parser")
print(doc.find_all('ytd-metadata-row-container-renderer', {"class": "style-scope ytd-watch-metadata"}))