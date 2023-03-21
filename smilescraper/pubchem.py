from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import chromedriver_binary

from smilescraper.logger import logging
from smilescraper.exception import CustomException
import sys
import pandas as pd
import streamlit as st

import time

logging.basicConfig(level=logging.INFO)

WAIT_TIME = 3

def get_driver():
    """Start Selenium Chrome Driver

    Returns:
        driver: Chrome Driver
    """
    option = webdriver.ChromeOptions()
    # option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    # service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(ChromeDriverManager(version= "112.0.5615.28").install(), options=option)
    return driver
    # try:
    #     # logging.info('Logging Started')
    #     # logging.info('Chrome Driver Starting')
    #     option = webdriver.ChromeOptions()
    #     option.add_argument('--headless')
    #     option.add_argument('--no-sandbox')
    #     service = Service(ChromeDriverManager().install())
    #     driver = webdriver.Chrome(options = option, service= service)
    #     return driver
    # except Exception as e:
    #     # logging.error('Error Occured in loading Driver')
    #     raise CustomException(error_msg= e, error_detail= sys)

# def get_driver():
#     """Start Selenium Chrome Driver

#     Returns:
#         driver: Chrome Driver
#     """
#     try:
#         logging.info('Chrome Driver Starting')
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         service = Service(ChromeDriverManager(version='111.0.5563.64').install())
#         driver = webdriver.Chrome(service=service, options=options)
#         return driver
#     except Exception as e:
#         logging.error('Error occurred in loading Driver')
#         raise e

def find_cas_number_link(start_link, driver):
    """_summary_

    Args:
        start_link (_type_): _description_
        driver (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        elements = WebDriverWait(driver, WAIT_TIME).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'span.breakword')))
        cid = elements[1].text
        n_link = start_link.split('#')[0]
        link = f"{n_link}compound/{cid}"
        return link
    except Exception as e:
        raise CustomException(error_msg= e, error_detail= sys)

# def find_cas_number_link(start_link, driver):
#     """_summary_

#     Args:
#         start_link (_type_): _description_
#         driver (_type_): _description_

#     Returns:
#         _type_: _description_
#     """
#     try:
#         logging.info(f'Finding CAS number link for {start_link}')
#         elements = WebDriverWait(driver, WAIT_TIME).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'span.breakword')))
#         cid = elements[1].text
#         print("CID {}".format(cid))
#         n_link = start_link.split('#')[0]
#         print("n_link {}".format(n_link))
#         link = f"{n_link}compound/{cid}"
#         print(link)
#         return link
#     except Exception as e:
#         logging.error(f'Error occurred in finding CAS number link for {start_link}')
#         raise e

def get_smile(data, driver, cas_no):
    """To get the smile formula.
    Args:
        data {dict}: dictionary to store information extracted from website.
        driver {selenium web driver}: to load the website and extract data.
    Returns:
        data {dict}: returns a dictionary of information stored.
    """
    try:
        element = WebDriverWait(driver, WAIT_TIME).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#Canonical-SMILES')))
        # Get the text of the element
        text = element.text
        split_text = text.split()
        canonical_smiles = split_text[2]
        data[cas_no] = canonical_smiles
    except Exception as e:
        # st.write('[INFO] Smile not found')
        data[cas_no] = 'None'
        raise CustomException(error_msg= e, error_detail= sys)

    return data

# def get_smile(data, driver, cas_no):
#     """To get the smile formula.

#     Args:
#         data {dict}: dictionary to store information extracted from website.
#         driver {selenium web driver}: to load the website and extract data.

#     Returns:
#         data {dict}: returns a dictionary of information stored.
#     """
#     try:
#         logging.info(f'Getting SMILES for {cas_no}')
#         # element = WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#Canonical-SMILES')))
#         # element = WebDriverWait(driver, WAIT_TIME).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#Canonical-SMILES')))
        
#         element = WebDriverWait(driver, WAIT_TIME).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#Canonical-SMILES')))
#         print(element)
#         canonical_smiles = element.text.split()[2]
#         data[cas_no] = canonical_smiles
#     except Exception as e:
#         logging.error(f'Error occurred in getting SMILES for {cas_no}')
#         data[cas_no] = 'None'
#     return data

def get_data(data, input_cas_list):
    """_summary_

    Args:
        data (_type_): _description_
        input_cas_list (_type_): _description_

    Returns:
        _type_: _description_
    """
    # start_time = time.time()
    count = 0
    for i in input_cas_list:           
        start_link = "https://pubchem.ncbi.nlm.nih.gov/#query=" + str(i)

        driver = get_driver()
        driver.set_page_load_timeout(60)
        driver.get(start_link)

        link = find_cas_number_link(start_link, driver)

        driver.get(link)
        data = get_smile(data, driver, cas_no= i)
        count += 1
        print('{} CAS Number is completed'.format(count))
    
    df = pd.DataFrame(list(data.items()), columns= ['Cas No', 'Smile'])
    # end_time = time.time()
    # st.write(end_time - start_time)
    return df
