from time import sleep
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd

from src.services.save_bedrooms import SaveBedrooms
from src.services.save_hotels import SaveHotels
from src.functions.bedrooms_functions import GetBedrooms
from src.functions.categories_functions import Categories
from src.functions.features_functions import Feature
from src.functions.number_functions import ExtractNumber


# Configure Chrome options
chrome_options = Options()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.headless = False
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Set the zone
today = datetime.today()

future_date1 = today + timedelta(days=30)
future_date2 = today + timedelta(days=31)

driver.get(f'https://www.booking.com/searchresults.es.html?ss=Medellín&ssne=Medellín&ssne_untouched=Medellín&efdco=1&label=gx-co-booking-booking-sd-pdsc&sid=3cb16c5170054bb6fc3437f5fe21f904&aid=348858&lang=es&sb=1&src_elem=sb&src=searchresults&dest_id=-592318&dest_type=city&checkin={future_date1.year}-{future_date1.month}-{future_date1.day}&checkout={future_date2.year}-{future_date2.month}-{future_date2.day}&ltfd=5%3A1%3A12-2024_2-2025%3A%3A&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure')

# Button validation
try:
    button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Ignorar información sobre el inicio de sesión." and @type="button"]')))
    button.click()
except:
    print("The button is not present in the page.")
    
# Load all cards    

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(2)  
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    
    
while True:
    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[span[text()='Cargar más resultados']]"))
        )
        button.click()
        sleep(1.5)
    except TimeoutException:
        print("The button with the text 'Load more results' is no longer present on the page or could not be loaded.")
        break
    
# Dataframes

column_names = [
    "date",
    "future_date",
    "hotel_title",
    "hotel_address",
    "neighborhood",
    "hotel_puntuation",
    "hotel_reviews",
    "services",
    "staff", 
    "installations_services", 
    "cleaning", 
    "confort", 
    "value_for_money", 
    "location", 
    "wifi", 
    "features"
]
            
hotels_df = pd.DataFrame(columns=column_names)

column_names = [
    "date",
    "future_date",
    "title_hotel",
    "title_room",
    "square_meter",
    "total_individual_beds",
    "total_doble_beds",
    "total_bunks",
    "total_sofa_beds",
    "bedrooms",
    "living_rooms",
    "max_capacity_room",
    "price_room",
    "breakfast_room",
    "features_room",
]

bedrooms_df = pd.DataFrame(columns=column_names)

total_hotels = 0
    
def Scraping(hotel_links):
    global bedrooms_df
    global future_date1
    j = 1            
    for link in hotel_links:
        errors = []
        #Puntuation
        try:
            hotel_puntuation = link.find_element(By.XPATH, ".//div[contains(text(), 'Puntuaci')]").text
        except Exception  as e:
            errors.append("<-> Error in puntuation")
        #Reviews
        try:
            hotel_reviews = link.find_element(By.XPATH, ".//div[contains(text(), 'comentarios')]").text
        except Exception  as e:
            errors.append("<-> Error in views") 
    
        try:
            link_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(link))
            link_element.click()
        except Exception as e:
            errors.append(f"<-> Error clicking the link: {e}") 
            continue
        
        try:
            WebDriverWait(driver, 30).until(EC.number_of_windows_to_be(2))
        except Exception as e:
            errors.append(f"<-> New window did not open: {e}") 
            continue
        
        sleep(2)
        
        driver.switch_to.window(driver.window_handles[1])
        
        sleep(1.5)
        
        #Title  
        try:
            hotel_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'pp-header__title')]"))).text
        except:
            errors.append("<-> There is not title for this hotel.") 
        #Address    
        try:
            hotel_address = driver.find_element(By.XPATH, '//*[@id="showMap2"]/span[1]').text
        except:
            errors.append("<-> There is not address for this hotel.") 
        #Servicios
        services = []    
        try:
            hotel_services_container = driver.find_element(By.XPATH, '//div[@data-testid="property-most-popular-facilities-wrapper"]')
            
            hotel_services = hotel_services_container.find_elements(By.XPATH, ".//li")

            for service in hotel_services:
                new_service = ""
                try:     
                    new_service = service.find_element(By.XPATH, ".//div/div/div/span/div/span").text
                except Exception as e:
                    try:
                        new_service = service.find_element(By.XPATH, ".//div/div/div/span/span/button/div/span").text
                    except Exception  as e:
                        errors.append("<-> Error in a special services") 
                if new_service != "" :
                    services.append(new_service) 
        except Exception  as e:
            errors.append("<-> Error in services") 
            
        #Bedrooms    
        bedrooms = GetBedrooms(driver, hotel_title.strip())
        bedrooms_df = pd.concat([bedrooms_df, bedrooms["bedrooms_df"]  ], ignore_index=True)
        errors.extend(bedrooms["errors"])
        
        #Categories
        categories = Categories(driver)
        errors.extend(categories["errors"])
            
        #Features
        features = Feature(driver)
        errors.extend(features["errors"])
            
        
        current_date = datetime.now()
        address_parts = hotel_address.split(",")
        neighborhood = address_parts[1].strip()

        new_row = {
            "date": current_date.strftime('%d/%m/%Y'),
            "future_date" : future_date1.strftime('%d/%m/%Y'),
            "hotel_title" : hotel_title.strip(),
            "hotel_address" : hotel_address,
            "neighborhood" : neighborhood,
            "hotel_puntuation" : hotel_puntuation.replace("Puntuación:", "").strip(),
            "hotel_reviews" : ExtractNumber(hotel_reviews),
            "services" : list(set(services)),
            "staff" : categories['staff'],
            "installations_services" : categories['installations_services'],
            "cleaning" : categories['cleaning'],
            "confort" : categories['confort'],
            "value_for_money" : categories['value_for_money'],
            "location" : categories['location'],
            "wifi" : categories['wifi'],
            "features" : features["features"]
        }

        hotels_df.loc[len(hotels_df)] = new_row
        
        print( f"{j} of {total_hotels} ---------------------------------------")
        print("Hotel", hotel_title)
        
        #End 
        driver.close()
        sleep(1)
        driver.switch_to.window(driver.window_handles[0])
        sleep(1)
        j += 1

def ExtractLinks():
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='property-card']")))
    return driver.find_elements(By.XPATH, "//div[@data-testid='property-card']")

try:
    next = driver.find_element(By.XPATH, "//button[@class='a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 deab83296e bb803d8689 a16ddf9c57']")

    condicion = True

    while condicion:
        
        hotel_links_page = ExtractLinks()
        total_hotels = len(hotel_links_page)
        Scraping(hotel_links_page)
        sleep(5)
        
        print("Scraped page!")
        
        if next.get_attribute('disabled') is None:
            condicion = False
        else:
            next.click()
            sleep(5)
        
    print("Done! v1")
except Exception  as e:
    hotel_links_page = ExtractLinks()
    total_hotels = len(hotel_links_page)
    sleep(5)
    Scraping(hotel_links_page)   
    print("Scraped page!")   
    print("Done! v2") 

SaveHotels(hotels_df)
SaveBedrooms(bedrooms_df)

driver.quit()