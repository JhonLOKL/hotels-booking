import re
from time import sleep
from datetime import datetime, timedelta
import pandas as pd
from selenium.webdriver.common.by import By
from src.functions.number_functions import ExtractNumber

def GetBedrooms(driver, title_hotel, future_date1):
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

    i = 0
    errors = []
    try:
        bedrooms_table = driver.find_element(By.XPATH, "//table[@id='hprt-table']")
        tbody = bedrooms_table.find_element(By.XPATH, ".//tbody")
        trs = tbody.find_elements(By.XPATH, ".//tr")
    
        previous_title_room = ""
        features_room = []
        first_square_meter_feature = ""
            
        for tr in trs:
            try:
                title_room = tr.find_element(By.XPATH, ".//span[@class='hprt-roomtype-icon-link ']").text
                previous_title_room = title_room
                
                try:
                    
                    total_individual_beds = 0
                    total_doble_beds = 0
                    total_bunks = 0
                    total_sofa_beds = 0
                    individual_pattern = re.compile(r'(\d+)\s+cama(?:s?)\s+individual(?:es?)')
                    doble_pattern = re.compile(r'(\d+)\s+cama(?:s?)\s+doble(?:s?)')
                    bunks_pattern = re.compile(r'(\d+)\s+litera(?:s?)')
                    sofa_bed_pattern = re.compile(r'(\d+)\s+sof(?:á|a)?(?:s?)\s+cama(?:s?)')
                    
                    beds = tr.find_elements(By.XPATH, ".//span[(contains(text(), 'cama') or contains(text(), 'litera')) and not(contains(@class, 'hprt-roomtype-icon-link ')) and not (contains(text(), 'Enchufe'))]")
                    for bed in beds:
                        
                        beds_text = bed.text.lower()
                        individual_matches = individual_pattern.findall(beds_text)
                        for match in individual_matches:
                            total_individual_beds += int(match)
                            
                        doble_matches = doble_pattern.findall(beds_text)
                        for match in doble_matches:
                            total_doble_beds += int(match)

                        bunks_matches = bunks_pattern.findall(beds_text)
                        for match in bunks_matches:
                            total_bunks += int(match)
                            
                        sofa_beds_matches = sofa_bed_pattern.findall(beds_text)
                        for match in sofa_beds_matches:
                            total_sofa_beds += int(match)
                        
                    bedrooms = tr.find_elements(By.XPATH, ".//strong[contains(text(), 'Dormitorio')]")
                    if bedrooms:
                        match = re.search(r'Dormitorio (\d+)', bedrooms[-1].text)
                        last_bedroom = int(match.group(1))
                    else:
                        last_bedroom = "1"
                        
                    living_rooms_container = tr.find_elements(By.XPATH, ".//strong[contains(text(), 'Sala de estar')]")
                    if living_rooms_container:
                        living_rooms = len(living_rooms_container)
                    else:
                        living_rooms = "0"
                        
                except:
                    total_individual_beds = 0
                    total_doble_beds = 0
                    total_bunks = 0
                    total_sofa_beds = 0
                
                try:   
                    show_more_button = tr.find_element(By.LINK_TEXT, "Más")
                    show_more_button.click()
                    sleep(1)
                except:
                    errors.append("<-> There is no show more button")
                    
                try:
                    features_contianer = tr.find_element(By.XPATH, ".//div[@class='hprt-roomtype-block']")
                    features = features_contianer.find_elements(By.XPATH, ".//span")
                    features_room = []
                    for feature in features:
                        features_room.append(feature.text)
                    features_room = list(dict.fromkeys(features_room))
                except:
                    print("<-> Error in features room")
            except:
                title_room = previous_title_room
                
            max_capacity_room = tr.find_element(By.XPATH, ".//span[contains(text(), 'personas')]").text
            price_room =tr.find_element(By.XPATH, ".//span[contains(text(), 'COP')]").text
            try:
                breakfast_room =  tr.find_element(By.XPATH, ".//span[contains(text(), 'Desayuno')]").text
            except Exception  as e:
                breakfast_room = ""

            for feature in features_room:
                if 'm²' in feature:
                    first_square_meter_feature = feature.replace(' m²', '').strip()
                    features_room.remove(feature)
                    break
            
            current_date = datetime.now()
            
            i += 1
            new_row = {
                "date": current_date.strftime('%d/%m/%Y'),
                "future_date" : future_date1.strftime('%d/%m/%Y'),
                "title_hotel" : title_hotel,
                "title_room" : title_room,
                "square_meter" : first_square_meter_feature,
                "total_individual_beds" : total_individual_beds,
                "total_doble_beds" : total_doble_beds,
                "total_bunks" : total_bunks,
                "total_sofa_beds" : total_sofa_beds,
                "bedrooms" : last_bedroom,
                "living_rooms" : living_rooms,
                "max_capacity_room" : ExtractNumber(max_capacity_room),
                "price_room" : ExtractNumber(price_room.replace(".", "")),
                "breakfast_room" : breakfast_room,
                "features_room" : features_room,
                }

            bedrooms_df.loc[len(bedrooms_df)] = new_row
    except:
        print("<-> Error table")
        
    return { "i": i,"bedrooms_df" : bedrooms_df, "errors":errors}

def GetPricesBedrooms(driver, title_hotel, future_date1):
    column_names = [
    "date",
    "future_date",
    "title_hotel",
    "title_room",
    "price_room",
    ]

    bedroomsPrices_df = pd.DataFrame(columns=column_names)

    i = 0
    errors = []
    try:
        bedrooms_table = driver.find_element(By.XPATH, "//table[@id='hprt-table']")
        tbody = bedrooms_table.find_element(By.XPATH, ".//tbody")
        trs = tbody.find_elements(By.XPATH, ".//tr")

        previous_title_room = ""
            
        for tr in trs:
            try:
                title_room = tr.find_element(By.XPATH, ".//span[@class='hprt-roomtype-icon-link ']").text
                previous_title_room = title_room           
            except:
                title_room = previous_title_room
                
            price_room =tr.find_element(By.XPATH, ".//span[contains(text(), 'COP')]").text
            
            current_date = datetime.now()
            
            i += 1
            new_row = {
                "date": current_date.strftime('%d/%m/%Y'),
                "future_date" : future_date1.strftime('%d/%m/%Y'),
                "title_hotel" : title_hotel,
                "title_room" : title_room,
                "price_room" : ExtractNumber(price_room.replace(".", "")),
                }

            bedroomsPrices_df.loc[len(bedroomsPrices_df)] = new_row
    except:
        print("<-> Error table")
        
    return { "i": i,"bedroomsPrices_df" : bedroomsPrices_df, "errors":errors}