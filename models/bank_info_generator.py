import requests
from bs4 import BeautifulSoup
import re
import traceback
from models.errors import IbanError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import logging
from fake_headers import Headers

class BankInfoGenerator:

    def __init__(self, iban) -> None:
        self.iban = iban.upper()
    
    def get_bank_info(self):
        if self.iban[:2] == "IT" or self.iban[:2] == "ES":
            return self.ibancalculator_parser()
        elif self.iban[:2] == "PT":
            return self.bank_codes_parser()
    

    def ibancalculator_parser(self):
        try:
            data = {
                "tx_valIBAN_pi1[iban]" : self.iban, # номер ибана
                "tx_valIBAN_pi1[fi]" : "fi", # не изменяемый параметр
                "no_cache" : "1", # не изменяемый параметр
                "Action" : "validate+IBAN,+look+up+BIC", # не изменяемый параметр
            }
            
            headers = {
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Content-Type" : "application/x-www-form-urlencoded"
            }
            
            resp = requests.post("https://www.ibancalculator.com/iban_validieren.html", data=data, headers=headers)

            soup = BeautifulSoup(resp.text, "lxml")
            
            field1 = soup.find_all("fieldset")
            if len(field1) > 2:
                field1 = field1[1]
            else:
                raise IbanError("Номер ибана содержит ошибку") 
            
            country = self.iban[:2].upper()

            if country == "IT":
                code_account_tag = field1.find_all('p')[1]
                bank_code = field1.find_all('p')[3]
            elif country == "ES":
                code_account_tag = field1.find_all('p')[2]
                bank_code = field1.find_all('p')[1]
            else:
                raise IbanError("Указана неверная страна в номере Ибана")
            
            if code_account_tag:
                code_account_numbers = re.findall(r'\d+', str(code_account_tag))
                bank_code_numbers = re.findall(r'\d+', str(bank_code))
            else:
                raise IbanError("Не найден код аккаунта") 

            result = soup.find_all("fieldset")[2]
            
            adress = result.find_all('p')[4]
            adress_text = ', '.join(adress.stripped_strings)

            brunch = result.find_all('p')[5]

            name = result.find_all('p')[3]
            name = name.text.replace("Bank: ", "")

            bic = result.find_all('p')[2]
            bic = bic.text.replace("BIC: ", "").replace("BIC into the clipboard", "")


            # Если тег найден, извлечем число из текста
            if brunch:
                branch_number_text = brunch.find('b').next_sibling.strip()
                branch_number = branch_number_text.replace('Branch number:', '').strip()

                
            else:
                raise IbanError("Информация о Branch number не найдена.") 
            return {
                "adress" : adress_text, 
                "branch_number" : branch_number, 
                "code_account" : code_account_numbers[0],
                "bank_code" : bank_code_numbers[0],
                "name" : name,
                "bic" : bic,
                }
        
        except Exception as e:
            return e
        
    def bank_codes_parser(self):
        headers = Headers(browser="chrome", os="win").generate()
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

        # chrome_driver = 'chromedriver-win-x64.exe'
        options = Options()
        options.add_argument('--headless') 
        options.add_argument('--no-sandbox')
        options.add_argument(f"user-agent={headers['User-Agent']}")

        driver = webdriver.Chrome(options=options)
        try:
            # driver.maximize_window()
            driver.get("https://bank.codes/iban/validate/")
            # time.sleep(70)
            # Ожидание загрузки элементов 
            iban_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/section[1]/div/div/div[1]/div/form/div/input[1]"))
            )
            iban_input.send_keys(self.iban)

            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]'))  
            )
            cookie_button.click()

            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[2]/section[1]/div/div/div[1]/div/form/div/input[2]"))  
            )
            submit_button.click()

            # Явное ожидание загрузки страницы
            WebDriverWait(driver, 10).until(
                EC.title_contains("IBAN")  
            )
            
            logging.info("Page loaded successfully")

            page_source = driver.page_source


        except Exception as e:
            logging.exception(e)

        finally:
            driver.quit()

        try:

            soup = BeautifulSoup(page_source, "lxml")

            # Извлекаем значение для "Bank Name"
            bank_name = soup.find('dt', string='Bank Name').find_next('dd').text.strip()

            # Извлекаем значение для "Address"
            address = soup.find('dt', string='Address').find_next('dd').text.strip()

            # Извлекаем значение для "BIC"
            bic = soup.find('dt', string='SWIFT Code').find_next('dd').text.strip()

            # Извлекаем значение для "brunch number"
            bank_code = soup.find('dt', string='Bank Code').find_next('dd').text.strip()

            # Извлекаем значение для "Account Number"
            account_number = soup.find('dt', string='Account Number').find_next('dd').text.strip()
        
            brunch_number = '0003'

            return {
                "adress" : address, 
                "branch_number" : brunch_number, 
                "code_account" : account_number,
                "bank_code" : bank_code,
                "name" : bank_name,
                "bic" : bic,
            }
        except Exception as e:
            raise IbanError('Информация IBAN не корректна')