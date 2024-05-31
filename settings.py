import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()


class SiteSettings:
    api_key = os.getenv('SITE_API', None)
    host_api = os.getenv('HOST_API', None)
    token = os.getenv('TOKEN', None)


class SearchSettings:
    id_map = {}
    children = []


site = SiteSettings()
search = SearchSettings()