import aiohttp
from typing import Union

from loader import KEITARO_IP, KEIARO_ADMIN_TOKEN
from data import UserService

"""
Модуль для работы с Keitaro API
"""

class Keitaro:
    
    def __init__(self,  token: str) -> None:
        self.head = {"Api-Key": f"{token}"}

    async def cheсk_token(self)-> bool:
        """
        Проверка токена
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://{KEITARO_IP}/admin_api/v1/groups?type=campaigns', headers=self.head) as resp:
                    if 'error' in await resp.json():
                        return False
                    else:
                        return True
        except Exception:
            return False

    async def _get_all_keitaro_campaigns(self) -> Union[dict, list]:
        """
        Получение списка кампаний

        Returns:
        -------
            dict: ответ на GET запрос
            list: возвращает пустой массив при неудачном запросе
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://{KEITARO_IP}/admin_api/v1/campaigns', headers=self.head) as resp:
                    if 'error' not in await resp.json():
                        return await resp.json()
                    else:
                        return []
        except:
            return await self._get_all_keitaro_campaigns()
        
    async def get_all_keitaro_groups(self) -> Union[dict, list]:
        """
        Получение списка групп

                Args:
        -------
          id: int
            id кампании

        Returns:
        -------
            dict: ответ на GET запрос
            list: возвращает пустой массив при неудачном запросе
        """
        try:
             async with aiohttp.ClientSession() as session:
                async with session.get(f'http://{KEITARO_IP}/admin_api/v1/groups?type=campaigns', headers=self.head) as resp:
                    if 'error' not in await resp.json():
                        return await resp.json()
                    else:
                        return []
        except:
            return await self.get_all_keitaro_groups()
        
    async def clone_campaign(self, id: int) -> Union[dict, list]:
        """
        Клонирование кампании

        Args:
        -------
          id: int
            id кампании

        Returns:
        -------
            dict: ответ на GET запрос
            list: возвращает пустой массив при неудачном запросе
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f'http://{KEITARO_IP}/admin_api/v1/campaigns/{id}/clone', headers=self.head) as resp:
                    if len(await resp.json()) != 0:
                        if 'error' not in await resp.json():
                            return await resp.json()
                        else:
                            return []  
                    else:
                        return []
        except:
            return await self.clone_campaign(id)
        
    async def rename_campaign(self, id:int , new_name: str) -> dict:
        """
        Переименование кампании

        Args:
        -------
            id: int
                id компании в Keitaro
            new_name: str
                Новое имя кампании
        
        Returns:
        -------
            dict: ответ на GET запрос, если он неудачный, пустой словарь.
        """
        try:
            async with aiohttp.ClientSession() as session:
                body = {'name': new_name, "group_id": 20}
                async with session.put(f'http://{KEITARO_IP}/admin_api/v1/campaigns/{id}', headers=self.head, json=body) as resp:
                    if 'error' not in await resp.json():
                        return await resp.json()
                    else:
                        return {}
        except:
            return await self.rename_campaign(id, new_name)
        
    async def get_user_campany(self) -> list:
        """
        Получение списка кампаний пользователя
        """
        res = await self._get_all_keitaro_campaigns()
        ready_company = []
        company_list = [company['name'] for company in res] 
        for company in company_list:
            if 'Основа' in company and 'Copy' not in company:
                ready_company.append(company)
        return ready_company
    
    @staticmethod
    async def get_all_campanies_users() -> dict:
        """"
        Получение всех пользователей и их кампаний
        """
        resp_data =  UserService.get_all()
        tokens = resp_data["tokens"]
        sub = resp_data["subs"]
        res = {}
        for token, sub in zip(tokens, sub):
            camp = ""
            head = {"Api-Key": token}
            async with aiohttp.ClientSession() as session:
                async with session.get(f'http://{KEITARO_IP}/admin_api/v1/campaigns', headers=head) as resp:
                    lst_campaign = ['[' + str(campaign['id']) + '] ' + campaign['name'] for campaign in await resp.json()]
                    for campaign in lst_campaign:
                        if 'Основа' in campaign:
                            camp += f"🔹 {campaign} \n"
                    res[f"🔶 {sub} 🔶"] = camp
        return res
    
    @staticmethod
    async def get_all_campanies() -> dict:
        """
        Возвращает список всех активных кампаний
        """
        resp_data =  UserService.get_all()
        tokens = resp_data["tokens"]
        dct_active_campaigns = {}
        msg = '🔶 Список активных кампаний 🔶' + '\n'
        for token in tokens:
            async with aiohttp.ClientSession() as session:
                head = {"Api-Key": token}
                async with session.get(f'http://{KEITARO_IP}/admin_api/v1/campaigns', headers=head) as resp:
                    dct_campaign = {campaign['id']: campaign['name'] for campaign in await resp.json()}
                    for key, value in dct_campaign.items():
                        if 'Основа' in value:
                            dct_active_campaigns.update({key: value})
        dct_active_campaigns = dict(sorted(dct_active_campaigns.items()))
        for k, v in dct_active_campaigns.items():
             msg = msg + '🔹 [' + str(k) + '] ' + v + '\n'
        return msg
    
    @staticmethod
    async def get_all_offers() -> dict:
        resp_data =  UserService.get_all()
        tokens = resp_data["tokens"]
        dct_active_campaigns = {}
        dct_campaign = {}
        msg = '🔶 Список активных офферов 🔶' + '\n'
        for token in tokens:
            async with aiohttp.ClientSession() as session:
                head = {"Api-Key": token}
                async with session.get(f'http://{KEITARO_IP}/admin_api/v1/campaigns', headers=head) as resp:
                    dct_campaign = {campaign['id'] : campaign['name'] for campaign in await resp.json()}
        
            for key, value in dct_campaign.items():
                if 'Основа' in value:
                    dct_active_campaigns.update({key: value})
                   
        dct_active_campaigns = dict(sorted(dct_active_campaigns.items()))

        dct_active_offers = {}
        for key, value in dct_active_campaigns.items():
            async with aiohttp.ClientSession() as session:
                head = {"Api-Key": KEIARO_ADMIN_TOKEN}
                async with session.get(f'http://{KEITARO_IP}/admin_api/v1/campaigns/{key}/streams', headers=head) as resp:
                    response_data = await resp.json()
                    for i in range(0, len(response_data)):
                        if len(response_data[i]['offers'])!= 0:
                            for j in range(0, len(response_data[i]['offers'])):
                                if response_data[i]['offers'][j]['share']!= 0:
                                    dct_active_offers.update({response_data[i]['offers'][j]['offer_id']: ''})

        for key in dct_active_offers.keys():
            async with aiohttp.ClientSession() as session:
                head = {"Api-Key": KEIARO_ADMIN_TOKEN}
                async with session.get(f'http://{KEITARO_IP}/admin_api/v1/offers/{key}', headers=head) as resp:
                    json_data = await resp.json()
                    dct_active_offers[key] = json_data['name']
        
        for key, value in dct_active_offers.items():
            msg = msg + '🔹 [' + str(key) + '] ' + value + '\n'

        return msg
