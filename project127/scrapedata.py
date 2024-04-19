from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# browser = webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
# browser.get(START_URL)
time.sleep(10)
scrapped_data=[]

def scrape(hyperlink):
    try: 
        page = requests.get(hyperlink)
        bright_star_table = BeautifulSoup.find("tr", attrs=("class", "Field brown dwarfs"))
        temp_list = []

        for tr_tag in bright_star_table.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
            scrapped_data.append(temp_list)
    except: 
        time.sleep(1)
        scrape(hyperlink)

stars_data=[]

for i in range(0, len(scrapped_data)):
    star_names = scrapped_data[i][1]
    distance = scrapped_data[i][3]
    mass = scrapped_data[i][5]
    radius = scrapped_data[i][6]
    lum = scrapped_data[i][7]
    require_data = [star_names, distance, mass, radius, lum]
    stars_data.append(require_data)
headers = ['star_name', 'distance', 'mass', 'radius', 'luminosity']
star_df_1 = pd.DataFrame(stars_data, columns=headers)
star_df_1.to_csv('scrapped_data.csv', index=True, index_label="id")