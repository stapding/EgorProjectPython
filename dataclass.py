from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:
    Id: str
    Name: str
    Price: int
    Count: int
    Category: dict
    Url: str


    @staticmethod
    def deserialize_product(dict):
        return Product(dict['Id'],dict['Name'],dict['Price'],dict['Count'],dict["Category"],dict["Url"])

@dataclass
class Order:
    id: int
    products: list
    date: datetime
    user: dict

    @staticmethod
    def deserializer(data: dict):
        if isinstance(data,dict):
            products = []
            for value in data['products']:
                products.append(Product.deserialize_product(value))
            return Order(data['id'],products, data['date'],data['user'])