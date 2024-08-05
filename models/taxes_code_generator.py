import traceback
import requests
from bs4 import BeautifulSoup
from random import randint

class TaxesCodeGenerator():
    @staticmethod
    def italy(name: str, lastname: str, day_birth: str, mon_birth: str, year_birth: str, sex: str) -> str:
        try:
            data = {
                "cg" : name, # имя
                "nm" : lastname, # фамилия
                "gg" : str(day_birth), # день рождения
                "mm" : str(mon_birth), # месяц рождения
                "aa" : str(year_birth), # год рождения
                "ss" : sex, # Пол
                "lg" : "TEANA (PZ)", # Место рождения
                "cb" : "", # не изменяемый параметр
                "dv" : "", # не изменяемый параметр
                "ac" : "1", # не изменяемый параметр
            }
            
            headers = {
                "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Content-Type" : "application/x-www-form-urlencoded"
            }
            
            resp = requests.post("https://zip-codes.nonsolocap.it/codice-fiscale/", data=data, headers=headers)
            
            soup = BeautifulSoup(resp.text, "lxml")
            result = soup.find("input", class_="form-control sz").get("value")
            return result
        
        except Exception as e:
            traceback.print_exc()
            return e

    @staticmethod
    def spain() -> str:
        resp = requests.get("https://generator.avris.it/api/ES/nif")
        return resp.text.replace('"', '')

    @staticmethod
    def portugal() -> str:
        nine_digit_number = randint(100000000, 999999999)
        return nine_digit_number