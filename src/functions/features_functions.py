from selenium.webdriver.common.by import By

def Feature(driver):
    features = []
    errors = []
    try:
        features_container = driver.find_element(By.XPATH, '//section[@id="hp_facilities_box"]')
        lis = features_container.find_elements(By.XPATH, './/li')
        for li in lis:
            features.append(li.text)
    except Exception  as e:
        errors.append("<-> Error in features")
    return{
        "features" : features,
        "errors" : errors
    }