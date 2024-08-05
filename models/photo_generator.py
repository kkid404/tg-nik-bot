import traceback
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2
import numpy as np
from random import randint
from models.errors import BankError, IbanError
from models.taxes_code_generator import TaxesCodeGenerator
from utils.bank_info import bank_info
from models.bank_info_generator import BankInfoGenerator

class PhotoGenerator():

    def __init__(self):
        self.FONT_PATH = "fonts/colibri/Calibri_Bold.TTF"
        # Определение констант для файлов и размеров шрифтов

        self.FONT_SIZE_MAIN = 25
        self.POSITION_NAME = (650, 370)
        self.POSITION_iban_PROFILE = (650, 415)
        self.POSITION_TAXES = (650, 495)
        self.OUTPUT_FILE = f"done_img{randint(111, 666)}.jpg"
        self.DEV_OUTPUT_FILE = "done_img.jpg"
        self.BANK_NAME_POSITION = (650, 455)
        self.BIC_POSITION = (650, 535)
        self.CODE_BANK_POSITION = (650, 575)
        self.BANK_ACCOUNT_POSITION = (650, 625)
        self.BANK_ADRESS_POSITION = (650, 675)
        self.BRUNCH_NUMBER_POSITION = (195, 195)

    def scan_effect(self, img_path, output_path, noise_factor=0.8):
        try:
            # Чтение изображения с использованием OpenCV
            img = cv2.imread(img_path)

            # Генерация случайного шума
            noise = np.random.normal(0, noise_factor, img.shape).astype(np.uint8)  # Конвертация в тот же тип данных, что и у изображения

            # Добавление шума к изображению
            noisy_image = cv2.add(img, noise)

            # Сохранение результата
            cv2.imwrite(output_path, noisy_image)

            return output_path
        except Exception as e:
            return e

    def spain_bank_statement_info(self):
        IMAGE_PATH = "img/example.jpg"
        taxes_code = TaxesCodeGenerator.spain()
        return {"image" : IMAGE_PATH, "taxes_code" : taxes_code}

    def portugal_bank_statement_info(self):
        IMAGE_PATH = "img/example_pt.jpg"
        taxes_code = TaxesCodeGenerator.portugal()
        return {"image" : IMAGE_PATH, "taxes_code" : taxes_code}

    def italy_bank_statement_info(self, name: str, lastname: str, day_birth: str, mon_birth: str, year_birth: str, sex: str):
        try:
            IMAGE_PATH = "img/example_it.jpg"
            taxes_code = TaxesCodeGenerator.italy(name, lastname, day_birth, mon_birth, year_birth, sex)
            return {"image" : IMAGE_PATH, "taxes_code" : taxes_code}
        except Exception as e:
            traceback.print_exc()
            return e
        
    
    def create_document(self, document_path, name, iban, taxes_code):
        try:
            iban = iban.upper().replace(" ", "")
            iban_info_generate  = BankInfoGenerator(iban)
            iban_info = iban_info_generate.get_bank_info()

            if len(iban_info["adress"]) <= 45:
                ADRESS_SIZE_MAIN = 25
            else:
                ADRESS_SIZE_MAIN = 16

            bank = iban_info["name"]

            if bank not in bank_info.keys():
                raise BankError("Банка нет в базе данных")
            
            logo_path = bank_info[bank]["logo_path"]

            if isinstance(iban_info, Exception):
                return iban_info

            with Image.open(document_path) as img:
                with  Image.open(logo_path) as logo:
                    bg_width, bg_height = img.size
                    # Масштабируем изображение для вставки (в данном случае, к 25% от размера основного)
                    logo = logo.resize((int(bg_width * bank_info[bank]["width"]), int(bg_height * bank_info[bank]["height"])))
                    img.paste(logo, bank_info[bank]["position_logo"])
                draw = ImageDraw.Draw(img)
                font_main = ImageFont.truetype(self.FONT_PATH, size=self.FONT_SIZE_MAIN)
                font_adress = ImageFont.truetype(self.FONT_PATH, size=ADRESS_SIZE_MAIN)
                
                draw.text(self.BRUNCH_NUMBER_POSITION, iban_info["branch_number"], fill="black", font=font_main)
                draw.text(self.POSITION_NAME, name, fill="black", font=font_main)
                draw.text(self.POSITION_iban_PROFILE, iban, fill="black", font=font_main)
                draw.text(self.POSITION_TAXES, str(taxes_code), fill="black", font=font_main)
                
                draw.text(self.BANK_NAME_POSITION, bank, fill="black", font=font_main)
                draw.text(self.BIC_POSITION, iban_info["bic"], fill="black", font=font_main)
                draw.text(self.CODE_BANK_POSITION, iban_info["bank_code"], fill="black", font=font_main)
                draw.text(self.BANK_ACCOUNT_POSITION, iban_info["code_account"], fill="black", font=font_main)
                draw.text(self.BANK_ADRESS_POSITION, iban_info["adress"], fill="black", font=font_adress)
                
                img.save(self.OUTPUT_FILE, quality=50)
                self.scan_effect(self.OUTPUT_FILE, self.OUTPUT_FILE)
                return self.OUTPUT_FILE
        
        except Exception as e:
            traceback.print_exc()
            return e
