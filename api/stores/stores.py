import requests
import random
import allure
from config.config_reader import Config


class Filters:
    def __init__(self, id: int = None, name: str = None, address: str = None, city_id: int = None,
                 city_name: str = None, region_id: int = None, region_name: str = None, store_type_id: [int] = None,
                 store_type_name: [str] = None, segment_id: [str] = None, external_id: [str] = None,
                 external_id2: [str] = None, territory1_id: [str] = None, territory: [str] = None,
                 retailer_id: [int] = None,
                 retailer_name: [str] = None, lon: [] = None, lat: [] = None, category: [str] = None,
                 type: [str] = None, active_matrices_count: [int] = None, dt_update: [str] = None):
        self.params = {
            "id": id,
            "name": name,
            "address": address,
            "city_id": city_id,
            "city_name": city_name,
            "region_id": region_id,
            "region_name": region_name,
            "store_type_id": store_type_id,
            "store_type_name": store_type_name,
            "segment_id": segment_id,
            "external_id": external_id,
            "external_id2": external_id2,
            "territory1_id": territory1_id,
            "territory": territory,
            "retailer_id": retailer_id,
            "retailer_name": retailer_name,
            "lon": lon,
            "lat": lat,
            "category": category,
            "type": type,
            "active_matrices_count": active_matrices_count,
            "dt_update": dt_update
        }

    def get_filters(self):
        return self.params


class Stores:
    def __init__(self):
        self.BASE_URL = Config.get_config().stand
    @allure.step('Вызов метода list_all_stores')
    def list_all_stores(self, auth_header, last_store_id: int = None, no_total: bool = None, limit: int = None,
                        offset: int = None, sort: str = None, filter: Filters = Filters()):
        params = {
            "last_store_id": last_store_id,
            "no_total": no_total,
            "limit": limit,
            "offset": offset,
            "sort": sort
        }
        params_request = {**params, **filter.get_filters()}
        response = requests.get(self.BASE_URL + '/api/v1/stores/', params=params_request, headers=auth_header)
        return response

    def list_all_stores_another_filters(self, auth_header, last_store_id: int = None, no_total: bool = None,
                                        limit: int = None,
                                        offset: int = None, sort: str = None, filters: {} = {}):
        params = {
            "last_store_id": last_store_id,
            "no_total": no_total,
            "limit": limit,
            "offset": offset,
            "sort": sort
        }
        params_request = {**params, **filters}
        response = requests.get(self.BASE_URL + '/api/v1/stores/', params=params_request, headers=auth_header)
        return response
    @allure.step('Получение случайной записи')
    def get_filters_data(self, auth_header):
        total = self.list_all_stores(auth_header).json()['total']
        all_data = self.list_all_stores(auth_header, limit=total).json()['data']
        return random.choice(all_data)


if __name__ == "__main__":
    response = Stores().list_all_stores({'Authorization': 'Bearer ed194783-cb29-4220-a78d-5d191aa6de1f'},
                                        no_total=False, limit=200)
    # response = Stores().get_filters_data({'Authorization': 'Bearer ed194783-cb29-4220-a78d-5d191aa6de1f'})
    print(response.json())
