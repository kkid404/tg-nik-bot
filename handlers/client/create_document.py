import os
import re
import traceback

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from models.errors import IbanError
from states import  DocumentCreateStorage
from keyboard import ClientKeyboard
from lang.ru import files
from models.photo_generator import PhotoGenerator
from utils.bank_info import bank_info


@dp.message_handler(text=files["keyboards"]["main"][2])
async def documents(message: types.Message, kb = ClientKeyboard()):
    await bot.send_message(
        message.from_user.id,
        files["messages"]["documents"],
        reply_markup= kb.documents_kb()
    )


@dp.message_handler(text=files["keyboards"]["documents"][0])
async def create_bank_chek(message: types.Message, state: FSMContext, kb = ClientKeyboard()):
    await bot.send_message(
        message.from_user.id,
        files["messages"]["name"],
        reply_markup= kb.back()
    )
    await DocumentCreateStorage.name.set()

@dp.message_handler(state=DocumentCreateStorage.name)
async def get_iban(message: types.Message, state: FSMContext, kb = ClientKeyboard()):
    
    async with state.proxy() as data:
        data["name"] = str(message.text).upper()

    await bot.send_message(
        message.from_user.id,
        files["messages"]["iban"],
        reply_markup= kb.back()
    )

    await DocumentCreateStorage.next()



@dp.message_handler(state=DocumentCreateStorage.iban)
async def get_bank(message: types.Message, state: FSMContext, kb = ClientKeyboard()):
    
    async with state.proxy() as data:
        data["iban"] = message.text

    if data["iban"][:2].upper() == "ES" or data["iban"][:2].upper() == "PT":
            try:
                photo = PhotoGenerator()
                name = data["name"]
                iban = data["iban"]
                if data["iban"][:2].upper() == "ES":
                    bank_info= photo.spain_bank_statement_info()
                elif data["iban"][:2].upper() == "PT":
                    bank_info= photo.portugal_bank_statement_info()

                taxes_code = bank_info["taxes_code"]
                document = bank_info["image"]

                create_document = photo.create_document(document, name, iban, taxes_code)

                if isinstance(create_document, Exception):
                    await bot.send_message(
                        message.from_user.id,
                        create_document,
                        reply_markup=kb.start_kb()
                        )
                    
                await state.finish()
                
                ready_document = open(create_document, "rb")
                await bot.send_photo(
                    message.from_user.id,
                    ready_document,
                    reply_markup=kb.start_kb()
                    )
                
                await state.finish()
                os.remove(create_document)
            
            except Exception as e:
                traceback.print_exc()
                await bot.send_message(
                    message.from_user.id,
                    files["messages"]["global_error"],
                    reply_markup=kb.start_kb()
                    )
                
                await state.finish()
    
    
    else:
        await bot.send_message(
            message.from_user.id,
            files["messages"]["date_birth"],
            reply_markup=kb.back()
        )
        await DocumentCreateStorage.next()

@dp.message_handler(state=DocumentCreateStorage.date_birth)
async def get_iban(message: types.Message, state: FSMContext, kb = ClientKeyboard()):
    
    async with state.proxy() as data:
        data["date_birth"] = message.text

    await bot.send_message(
        message.from_user.id,
        files["messages"]["sex"],
        reply_markup= kb.sex_kb()
    )

    await DocumentCreateStorage.next()

@dp.message_handler(state=DocumentCreateStorage.sex)
async def get_iban(message: types.Message, state: FSMContext, kb = ClientKeyboard()):
    
    async with state.proxy() as data:
        data["sex"] = message.text
    try: 
        photo = PhotoGenerator()
        
        try:
            name, lastname = data["name"].split()
        
        except ValueError:
            await bot.send_message(
                message.from_user.id,
                files["messages"]["value_error_name"],
                reply_markup=kb.start_kb()
            )
        
            await state.finish()
            return
        
        iban = data["iban"]

        try:
            day, month, year = data["date_birth"].split(".")
        except ValueError:
            await bot.send_message(
                message.from_user.id,
                files["messages"]["value_error_date"],
                reply_markup=kb.start_kb()
            )
        
            await state.finish()
            return


        sex = data["sex"].upper()
        if sex != "M" and sex != "F":
            await bot.send_message(
                message.from_user.id,
                files["messages"]["value_error_sex"],
                reply_markup=kb.start_kb()
            )
        
            await state.finish()
            return

        bank_info= photo.italy_bank_statement_info(name, lastname, day, month, year, sex)
        taxes_code = bank_info["taxes_code"]
        document = bank_info["image"]

        create_document = photo.create_document(document, f"{name} {lastname}", iban, taxes_code)
        if isinstance(create_document, Exception):
            await bot.send_message(
                message.from_user.id,
                create_document,
                reply_markup=kb.start_kb()
            )
                    
            await state.finish()
            return

        ready_document = open(create_document, "rb")
        await bot.send_photo(
            message.from_user.id,
            ready_document,
            reply_markup=kb.start_kb()
            )
        
        await state.finish()
        os.remove(create_document)
    
    except Exception as e:
        traceback.print_exc()
        await bot.send_message(
            message.from_user.id,
            files["messages"]["global_error"],
            reply_markup=kb.start_kb()
            )
        
        await state.finish()