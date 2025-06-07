from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import logging

logger = logging.getLogger(__name__)
def crawler() -> pd.DataFrame:
    logger.info("Instalando ChromeDriver...")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    logger.info("Acessando site...")
    driver.get("https://quotes.toscrape.com")

    df = pd.DataFrame(columns=['frase', 'autor', 'tags'])

    logger.info("Iterando sobre a página...")
    i = 0
    while True:
        for item in driver.find_elements(By.CLASS_NAME,'quote'):
            elem_quote = item.find_element(By.CLASS_NAME,'text')
            elem_autor = item.find_element(By.CLASS_NAME,'author')
            elem_tags = item.find_elements(By.CLASS_NAME,'tag')

            quote_text = elem_quote.text.strip('"')

            if elem_tags:
                tags = [tag.text for tag in elem_tags]
            else:
                tags = ["N/A"]

            df.loc[len(df)] = [
                quote_text,
                elem_autor.text,
                tags
            ]

        try:
            i += 1
            logger.info(f"Página {i} finalizada.")
            proximo = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, 'next')))
            proximo.find_element(By.TAG_NAME, 'a').click()
            WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.CLASS_NAME, 'quote')))
        except TimeoutException:
            logger.info("Leitura concluída!")
            break

    return df