import datetime

from main import ServerThread, MyWindow, MyWindow2
from dataclass import Order
import json

def test_decode_return_true():
    json = b'{"user":{"productIds":[],"Role":1,"Email":"egor@egor.com","Password":"123123Z#","Name":"Egor","Surname":"Odinczov","X":0,"Birthdate":"1991-02-24T00:00:00","Country":"\\u0420\\u043E\\u0441\\u0441\\u0438\\u044F","Photo":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},"products":[{"Id":1,"Name":"AK-74M","Price":1000,"Category":{"Id":1,"Name":null},"Count":1,"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},{"Id":2,"Name":"test","Price":1000,"Count":1,"Category":{"Id":1,"Name":null},"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"}],"date":"2023-11-24T10:11:39.6450943+05:00","id":"d6deda18-57e1-41df-8560-924f403359d0"}'
    order = ServerThread.decode(json)
    assert len(order.products) > 0

def test_decode_return_none():
    json = b'{"user":{"p":"Egor","Surname":"Odinczov","X":0,"Birthdat"1991-02-24T00:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},"products":[{"Id":1,"Name":"AK-74M","Price":1000,"Category":{"Id":1,"Name":null},"Count":1,"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},{"Id":2,"Name":"test","Price":1000,"Count":1}],"date":"2023-11-24T10:11:39.6450943+05:00","id":"d6deda18-57e1-41df-8560-924f403359d0"}'
    order = ServerThread.decode(json)
    assert order is None

def test_deserialize_result_true():
    json1 = b'{"user":{"productIds":[],"Role":1,"Email":"egor@egor.com","Password":"123123Z#","Name":"Egor","Surname":"Odinczov","X":0,"Birthdate":"1991-02-24T00:00:00","Country":"\\u0420\\u043E\\u0441\\u0441\\u0438\\u044F","Photo":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},"products":[{"Id":1,"Name":"AK-74M","Price":1000,"Category":{"Id":1,"Name":null},"Count":1,"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},{"Id":2,"Name":"test","Price":1000,"Count":1,"Category":{"Id":1,"Name":null},"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"}],"date":"2023-11-24T10:11:39.6450943+05:00","id":"d6deda18-57e1-41df-8560-924f403359d0"}'
    received_json = json1.decode('utf-8')
    received_data = json.loads(received_json)
    result = Order.deserializer(received_data)

    dict_result = result.__dict__
    dict_result["products"] = [x.__dict__ for x in dict_result["products"]]

    assert isinstance(result, Order) and result.__dict__ == received_data


def test_filter_order_return_true():
    json = b'{"user":{"productIds":[],"Role":1,"Email":"egor@egor.com","Password":"123123Z#","Name":"Egor","Surname":"Odinczov","X":0,"Birthdate":"1991-02-24T00:00:00","Country":"\\u0420\\u043E\\u0441\\u0441\\u0438\\u044F","Photo":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},"products":[{"Id":1,"Name":"AK-74M","Price":1000,"Category":{"Id":1,"Name":null},"Count":1,"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},{"Id":2,"Name":"test","Price":1000,"Count":1,"Category":{"Id":1,"Name":null},"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"}],"date":"2023-11-24T10:11:39.6450943+05:00","id":"d6deda18-57e1-41df-8560-924f403359d0"}'
    order = ServerThread.decode(json)
    filtered = list(MyWindow.filtered([order], datetime.date(2020, 1, 1)))
    assert len(filtered) > 0


def test_filter_order_return_0():
    json = b'{"user":{"productIds":[],"Role":1,"Email":"egor@egor.com","Password":"123123Z#","Name":"Egor","Surname":"Odinczov","X":0,"Birthdate":"1991-02-24T00:00:00","Country":"\\u0420\\u043E\\u0441\\u0441\\u0438\\u044F","Photo":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},"products":[{"Id":1,"Name":"AK-74M","Price":1000,"Category":{"Id":1,"Name":null},"Count":1,"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},{"Id":2,"Name":"test","Price":1000,"Count":1,"Category":{"Id":1,"Name":null},"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"}],"date":"2023-11-24T10:11:39.6450943+05:00","id":"d6deda18-57e1-41df-8560-924f403359d0"}'
    order = ServerThread.decode(json)
    filtered = list(MyWindow.filtered([order], datetime.date(2025, 1, 1)))
    assert len(filtered) == 0


def test_search_order_return_0():
    json = b'{"user":{"productIds":[],"Role":1,"Email":"egor@egor.com","Password":"123123Z#","Name":"Egor","Surname":"Odinczov","X":0,"Birthdate":"1991-02-24T00:00:00","Country":"\\u0420\\u043E\\u0441\\u0441\\u0438\\u044F","Photo":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},"products":[{"Id":1,"Name":"AK-74M","Price":1000,"Category":{"Id":1,"Name":null},"Count":1,"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},{"Id":2,"Name":"test","Price":1000,"Count":1,"Category":{"Id":1,"Name":null},"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"}],"date":"2023-11-24T10:11:39.6450943+05:00","id":"d6deda18-57e1-41df-8560-924f403359d0"}'
    order = ServerThread.decode(json)
    filtered = list(MyWindow2.search(order.products, "p"))
    assert len(filtered) == 0


def test_search_order_return_1():
    json = b'{"user":{"productIds":[],"Role":1,"Email":"egor@egor.com","Password":"123123Z#","Name":"Egor","Surname":"Odinczov","X":0,"Birthdate":"1991-02-24T00:00:00","Country":"\\u0420\\u043E\\u0441\\u0441\\u0438\\u044F","Photo":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},"products":[{"Id":1,"Name":"AK-74M","Price":1000,"Category":{"Id":1,"Name":null},"Count":1,"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"},{"Id":2,"Name":"test","Price":1000,"Count":1,"Category":{"Id":1,"Name":null},"Url":"C:\\\\Users\\\\Admin\\\\Downloads\\\\flag.jpg"}],"date":"2023-11-24T10:11:39.6450943+05:00","id":"d6deda18-57e1-41df-8560-924f403359d0"}'
    order = ServerThread.decode(json)
    filtered = list(MyWindow2.search(order.products, "test"))
    assert len(filtered) == 1
