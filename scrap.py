



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
from io import BytesIO
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

dir_plantas = Path(r"G:\ExtensionChrome\wewewe_model\growdiaries\northern-light-automatic")


import requests
import aiohttp
import asyncio
import logging

logging.basicConfig(filename='G:\ExtensionChrome\wewewe_model/example.log', encoding='utf-8',level=logging.INFO)
logger = logging.getLogger(__name__)

async def scrap_por_request():
    #QUERY
    punto_comienzo = 2760
    cantidad_iteracion = 20
    
    
    headers = {
         "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7,es;q=0.6,ja;q=0.5",
        "authorization": "Bearer g!m5I7GX3BPcHaUywUhxjrx7l",
        "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-access": "U2FsdGVkX18wFyZB0zl6TBtUYjlslGnSBVPZYugFJW3WlQnECyTpftILpFwT7IJj",
        "x-guest": "5vwqm4fgedb6h1jyz2fuzp",
        "x-origin": "",
        "x-pass": "",
        "x-rniq": "dd2oqagbtyw",
        "x-uniq": "c65bc43c86bc61d4dbd60ebc4fbb310e1c648ba60c40407729b1845d6c92b91a"
        
        }
       
    async with aiohttp.ClientSession() as session:
        while True:
  
            url = f"https://growdiaries.com/api/v1/seeds/1589/gallery?start={punto_comienzo}&limit=20&sortable=week_update&tags=photo"
            res = requests.get(url, headers = headers )        
            
            if(res.status_code != 200):
                logger.error(f"te caiste tio, i:{punto_comienzo} {url} ")
            
            #FALTA REVISAR CUANDO YA NO QUEDAN IMAGENES
            tasks = [descargar_imagen(session, data) for data in res.json()["data"]["items_gallery"]]
            await asyncio.gather(*tasks)
            time.sleep(10)
            
            logging.INFO(f"rango completo {punto_comienzo}")
            
            punto_comienzo += cantidad_iteracion  
            

img_headers = {
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
async def descargar_imagen(session, data):

    img_nombre = re.search("([\w\d\-_]+)(\.\w+)$", data["size_big"]).group(1)
    numero_semana = str(data["item_week"]["days"])
    id_post = re.search("(?<=\/diaries\/)\d+", data["item_diary"]["link"]).group()
    url_img = data["size_big"]
    
        
    async with session.get(url_img) as response:
        if response.status == 200:
            ruta_post = dir_plantas / numero_semana 
                    
            if(not os.path.exists(ruta_post)):
                os.mkdir(ruta_post)

            ruta_post = ruta_post / id_post
                        
            if(not os.path.exists(ruta_post)):
                os.mkdir(ruta_post)
            
            with open(ruta_post / (img_nombre + '.png'), 'wb') as f:
                f.write(await response.read())
                logger.info(f"\tImage from {url_img} downloaded successfully.")
        else:
            logger.error(f"\tFailed to download image from {url_img}. Status code: {response.status}")
    
    
    
loop = asyncio.get_event_loop()

# Schedule the main() function to run within the existing loop
asyncio.ensure_future(scrap_por_request())





def scrap_por_selenium():
    try:
        driver = webdriver.Chrome(options = chrome_options)
        driver.get(r"https://growdiaries.com/seedbank/royal-queen-seeds/northern-light-automatic/gallery")
        # driver.get(r"https://growdiaries.com/seedbank/fastbuds/gorilla-cookies-auto/gallery")
        
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.list > div[data-group='3']"))).click()  
        # lista = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.stag.tag_tree")))
        
        # lista.click()
        # time.sleep(1)
        
        #SEMANAS
        # lista.find_element(By.CSS_SELECTOR,"div.childs > div.child_row:nth-child(13)" ).click()
        
        
        driver.execute_script("let algo = document.querySelector('#app > div.popup_secure > div.btn.secondary.inverted');\
                              if(algo){algo.click()}")
        #ITERAR SOBRE RAZAS
        #NO TODAS LAS PLANTAS TIENEN LA MISMA CANTIDAD DE SEMANAS, AJUSTARSE A ESO
        
        #CREAR ALGO QUE PERMITA ALMACENAR QUE ESTA LISTO, TIPO CHECKLIST 
        
        while posts := WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.video_item:not(:has(.video_play))"))):
            time.sleep(2)
            for post in posts: 
                        
                img = post.find_element(By.CSS_SELECTOR,'img')           
                img_nombre =  re.search("([\w\d\-_]+)(\.\w+)$", img.get_attribute('src')).group(1)
                
                url_post = post.find_element(By.CSS_SELECTOR,'div.video_info>a.ttl').get_attribute('href')
                id_post = re.search("(?<=\/diaries\/)\d+", url_post).group()
                
                #CAMBIAR A PATH
                semana = post.find_element(By.CSS_SELECTOR, 'a.ttl').get_attribute("textContent")
                numero_semana = re.search("\d+",semana).group()
                
                ruta_post = dir_plantas / numero_semana 
                
                if(not os.path.exists(ruta_post)):
                    os.mkdir(ruta_post)
                #ESTO SE PUEDE COMPRIMIR
                ruta_post = ruta_post / id_post
                            
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

