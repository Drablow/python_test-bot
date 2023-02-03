from settings import SiteSettings
from site_API.utils.site_api_handler import SiteApiInterface

site = SiteSettings()
url = "https://" + site.host_api

headers = {
    "X-RapidAPI-Key": site.api_key.get_secret_value(),
    "X-RapidAPI-Host": site.host_api
}

url_dict = {
    'city_url': url + '/locations/search',
    'hotel_url': url + '/properties/list',
    'photo_url': url + '/properties/get-hotel-photos'
}

lang = 'ru_RU'

site_api = SiteApiInterface()

# if __name__ == "__main__":
#     site_api()
