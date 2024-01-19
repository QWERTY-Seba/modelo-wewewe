



from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import os
import time
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

ruta_driver = r"C:\Users\Seba\Documents\chromedriver.exe"

chrome_options =  Options() 
chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument(r"--user-data-dir=I:\SELENIUM_TEST_PROFILES")
chrome_options.add_argument("--profile-directory=Profile 4")

#El Selenium save_as_screenshot puede afectarse debido a si hay elementos en pantalla pero no estan completos
chrome_options.add_argument("--window-size=1920,850")

#CREAR JSON O SIMILAR PARA TENER LISTA DE PLANTAS A SCRAPEAR CON ESTADOS DE LAS FOTOS DESCARGADAS

dir_plantas = Path("G:\ExtensionChrome\wewewe_model\growdiaries\gorilla-cookies-auto")




try:
    driver = webdriver.Chrome(options = chrome_options)
    driver.get(r"https://growdiaries.com/seedbank/fastbuds/gorilla-cookies-auto/gallery")
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.list > div[data-group='3']"))).click()  
    lista = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.stag.tag_tree")))
    
    lista.click()
    time.sleep(1)
    lista.find_element(By.CSS_SELECTOR,"div.childs > div.child_row:nth-child(13)" ).click()
    
    
    driver.execute_script("let algo = document.querySelector('#app > div.popup_secure > div.btn.secondary.inverted');\
                          if(algo){algo.click()}")
    #ITERAR SOBRE RAZAS
    #NO TODAS LAS PLANTAS TIENEN LA MISMA CANTIDAD DE SEMANAS, AJUSTARSE A ESO
    #CREAR UNA SUB_CARPETA QUE CONTENGA SEMANA A LA QUE CORRESPONDE EL GRUPO
    #CREAR ALGO QUE PERMITA ALMACENAR QUE ESTA LISTO, TIPO CHECKLIST 
    
    while posts := WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.video_item:not(:has(.video_play))"))):
        for post in posts: 
                    
            img = post.find_element(By.CSS_SELECTOR,'img')           
            img_nombre =  re.search("([\w\d\-_]+)(\.\w+)$", img.get_attribute('src')).group(1)
            
            url_post = post.find_element(By.CSS_SELECTOR,'div.video_info>a.ttl').get_attribute('href')
            id_post = re.search("(?<=\/diaries\/)\d+", url_post).group()
            
            #CAMBIAR A PATH
            ruta_post = dir_plantas / id_post
            
            if(not os.path.exists(ruta_post)):
                os.mkdir(ruta_post)
            
            with open(ruta_post / (img_nombre + '.png'), 'wb') as f:
                f.write(img.screenshot_as_png)
            
            
                
            print(url_post, id_post)
        driver.execute_script('document.querySelectorAll(".video_item").forEach(e => e.remove())')
    #CREAR IMAGENES Y LUEGO HACER DELETE  
    

except Exception as e:
    print("1", e)
    # if 'driver' in locals():
    #     driver.quit()

