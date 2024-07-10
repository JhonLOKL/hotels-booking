from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def Categories(driver):
    staff = ""
    installations_services = ""
    cleaning = ""
    confort = ""
    value_for_money = ""
    location = ""
    wifi = ""
    errors = []

    try:
        categorie_container = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[h3[text()='Categorías:']]")))
    except Exception  as e:
        errors.append("<-> Eror in categorie container")
    try:
        parent_div = categorie_container.find_element(By.XPATH, "./parent::div")
    except Exception  as e:
        errors.append("<-> Error in parent div")
    try:
        children_div = parent_div.find_elements(By.XPATH, "./div")
        
        if len(children_div) >= 2:
            second_div = children_div[1] 
        
        divs = second_div.find_elements(By.XPATH, "./div/div")

        for div in divs:
            try:
                div_categories = div.find_elements(By.XPATH, "./div/div/div/div")
                
                title = div_categories[0].text
                punctuation = div_categories[1].text
                
                if(title == "Personal"):
                    staff = punctuation
                    
                elif(title == "Instalaciones y servicios"):
                    installations_services = punctuation
                            
                elif(title == "Limpieza"):
                    cleaning = punctuation
                    
                elif(title == "Confort"):
                    confort = punctuation
                    
                elif(title == "Relación calidad-precio"):
                    value_for_money = punctuation
                    
                elif(title == "Ubicación"):
                    location = punctuation
                            
                elif(title == "WiFi gratis"):
                    wifi = punctuation
            except Exception  as e:
                errors.append("<-> Error getting ./div/div/div/div")
    except Exception  as e:
        errors.append("<-> Error in childen div")
    return {
        "staff": staff,
        "installations_services": installations_services,
        "cleaning": cleaning,
        "confort": confort,
        "value_for_money": value_for_money,
        "location": location,
        "wifi": wifi,
        "errors": errors    
    }
