import pytest
from helper.dict_differ import DictDiffer
from api.stores.stores import Stores, Filters
from allure_commons._allure import title, epic, story

@epic("Проверка операций stores")
@story("Проверка базовых операций.")
class TestStores:
    @title("Проверка last_store_id. Параметры вызова : {last_store_id} ,{sort}")
    @pytest.mark.parametrize("last_store_id,sort", [(0, None), (6, "id,-date"), (139599, "id,territory")])
    def test_last_store(self, auth_header, last_store_id, sort):
        response = Stores().list_all_stores(auth_header=auth_header, last_store_id=last_store_id, sort=sort)
        print(response.json())
        assert response.status_code == 200
        assert response.json()['data'][0]['id'] > last_store_id

    @title("Проверка limit. Параметры вызова : {limit} ")
    @pytest.mark.parametrize("limit", (0, 100, 139599))
    def test_limit(self, auth_header, limit):
        response = Stores().list_all_stores(auth_header=auth_header, limit=limit)
        assert response.status_code == 200
        assert len(response.json()['data']) == limit

    @title("Проверка offset. Параметры вызова : {offset} ")
    @pytest.mark.parametrize("offset", (0, 100, 139599))
    def test_offset(self, auth_header, offset):
        response = Stores().list_all_stores(auth_header=auth_header, offset=offset)
        assert response.status_code == 200
        assert response.json()['data'][0]['id'] > offset

    @title("Проверка sort. Параметры вызова : {sort} ,{condition}")
    @pytest.mark.parametrize("sort,condition", [("name", [" ", "А", "Б"]), ("-name", ["Э", "Ю", "Я"])])
    def test_sort(self, auth_header, sort, condition):
        response = Stores().list_all_stores(auth_header=auth_header, sort=sort)
        assert response.status_code == 200
        assert response.json()['data'][0]['name'][0].upper() in condition

    @title("Проверка filter. Параметры вызова : {filter} ,{condition}")
    @pytest.mark.parametrize("filter,condition",
                             [(Filters(id=1), "id"), (Filters(address='Москва, Одинцово, Кошкина 82'), "address")])
    def test_filter(self, auth_header, filter, condition):
        response = Stores().list_all_stores(auth_header=auth_header, filter=filter)
        print(response.json())
        assert response.status_code == 200
        assert response.json()['data'][0][condition] == filter.get_filters()[condition]

    @title("Проверка filter по случайному объекту")
    def test_all_filters(self, auth_header):
        rnd_data = Stores().get_filters_data(auth_header)
        response = Stores().list_all_stores_another_filters(auth_header, filters=rnd_data)
        print(rnd_data)
        print(response.json())
        assert response.json()['total'] == 1
        assert response.json()['count'] == 1
        assert response.status_code == 200
        assert DictDiffer(rnd_data, response.json()['data'][0]), "Фильтр отработал некорректно."
