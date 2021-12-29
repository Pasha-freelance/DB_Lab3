import datetime
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, select, and_
from sqlalchemy.orm import relationship
from db import Orders, Session, engine


def recreate_database():
    Orders.metadata.drop_all(engine)
    Orders.metadata.create_all(engine)


class Shop(Orders):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    address = Column(String)
    manager_name = Column(String)
    manager_surname = Column(String)

    def __init__(self, shop_id, address, manager_name, manager_surname):
        self.id = shop_id
        self.address = address
        self.manager_name = manager_name
        self.manager_surname = manager_surname

    def __repr__(self):
        return "{:>10}{:>35}{:>15}{:>40}" \
            .format(self.id, self.address, self.manager_name, self.manager_surname)


class Product(Orders):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    photo_url = Column(String)
    shop_id = Column(Integer)

    def __init__(self, product_id, shop_id, photo_url, name):
        self.id = product_id
        self.name = name
        self.photo_url = photo_url
        self.shop_id = shop_id

    def __repr__(self):
        return "{:>10}{:>10}{:>50}{:>100}" \
            .format(self.id, self.shop_id, self.name, self.photo_url)


class Discount(Orders):
    __tablename__ = 'discount'
    id = Column(Integer, primary_key=True)
    percent = Column(Integer)
    duration = Column(Integer)

    def __init__(self, discount_id, percent, duration):
        self.id = discount_id
        self.percent = percent
        self.duration = duration

    def __repr__(self):
        return "{:>10}{:>15}{:>15}" \
            .format(self.id, self.percent, self.duration)


class Product_discount(Orders):
    __tablename__ = 'product_discount'
    id = Column(Integer, primary_key=True)
    discount_id = Column(Integer)
    product_id = Column(Integer)

    def __init__(self, key, product_id, discount_id):
        self.id = key
        self.discount_id = discount_id
        self.product_id = product_id

    def __repr__(self):
        return "{:>10}{:>15}{:>15}" \
            .format(self.id, self.product_id, self.discount_id)


class Model:
    def __init__(self):
        self.session = Session()
        self.connection = engine.connect()

    def find_pk_product(self, key_value: int):
        return self.session.query(Product).filter_by(id=key_value).first()

    def find_fk_product(self, key_value: int):
        return self.session.query(Product).filter_by(shop_id=key_value).first()

    def find_pk_shop(self, key_value: int):
        return self.session.query(Shop).filter_by(id=key_value).first()

    def find_pk_discount(self, key_value: int):
        return self.session.query(Discount).filter_by(id=key_value).first()

    def find_pk_product_discount(self, key_value: int):
        return self.session.query(Product_discount).filter_by(id=key_value).first()

    def find_fk_product_discount(self, key_value: int, table_name: str):
        if table_name == 'Product':
            return self.session.query(Product_discount).filter_by(product_id=key_value).first()
        if table_name == 'Discount':
            return self.session.query(Product_discount).filter_by(discount_id=key_value).first()

    def print_products(self):
        return self.session.query(Product).order_by(Product.id.asc()).all()

    def print_discounts(self):
        return self.session.query(Discount).order_by(Discount.id.asc()).all()

    def print_product_discount(self):
        return self.session.query(Product_discount).order_by(Product_discount.id.asc()).all()

    def print_shop(self):
        return self.session.query(Shop).order_by(Shop.id.asc()).all()

    ###
    def delete_data_product(self, key) -> None:
        self.session.query(Product).filter_by(id=key).delete()
        self.session.commit()

    def delete_data_discount(self, key) -> None:
        self.session.query(Discount).filter_by(id=key).delete()
        self.session.commit()

    def delete_data_product_discount(self, key) -> None:
        self.session.query(Product_discount).filter_by(id=key).delete()
        self.session.commit()

    def delete_data_shop(self, key) -> None:
        self.session.query(Shop).filter_by(id=key).delete()
        self.session.commit()

    def update_data_product(self, id_product: int, shop_id: int, photo_url: str, name: str) -> None:
        self.session.query(Product).filter_by(id=id_product) \
            .update({Product.shop_id: shop_id, Product.name: name, Product.photo_url: photo_url})
        self.session.commit()

    def update_data_discount(self, id_discount: int, percent: int, duration: int) -> None:
        self.session.query(Discount).filter_by(id=id_discount) \
            .update({Discount.percent: percent, Discount.duration: duration})
        self.session.commit()

    def update_data_product_discount(self, key: int, product_id: int, discount_id: int) -> None:
        self.session.query(Product_discount).filter_by(id=key) \
            .update({Product_discount.product_id: product_id, Product_discount.discount_id: discount_id})
        self.session.commit()

    def update_data_shop(self, id_shop: int, address: str, manager_name: str, manager_surname: str) -> None:
        self.session.query(Shop).filter_by(id=id_shop) \
            .update({Shop.address: address, Shop.manager_name: manager_name, Shop.manager_surname: manager_surname})
        self.session.commit()

    ####3

    def insert_data_product(self, id_product: int, name: str, photo_url: str, shop_id: int) -> None:
        product = Product(product_id=id_product, name=name, photo_url=photo_url, shop_id=shop_id)
        self.session.add(product)
        self.session.commit()

    def insert_data_discount(self, discount_id: int, percent: int, duration: int) -> None:
        discount = Discount(discount_id=discount_id, percent=percent, duration=duration)
        self.session.add(discount)
        self.session.commit()

    def insert_data_product_discount(self, key: int, product_id: int, discount_id: int) -> None:
        product_discount = Product_discount(key=key, product_id=product_id, discount_id=discount_id)
        self.session.add(product_discount)
        self.session.commit()

    def insert_data_shop(self, id_shop: int, address: str, name: str, surname: str) -> None:
        shop = Shop(shop_id=id_shop, address=address, manager_name=name, manager_surname=surname)
        self.session.add(shop)
        self.session.commit()

    #####
    def product_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute(
                "insert into public.product select (SELECT MAX(id)+1 FROM public.product), "
                "(SELECT id FROM public.shop LIMIT 1 OFFSET "
                "(round(random() *((SELECT COUNT(id) FROM public.shop)-1)))), "
                "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''),"
                "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), '');")

    def shop_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute(
                "insert into public.shop select (SELECT (MAX(id)+1) FROM public.shop), "
                "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''),"
                "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''),"
                "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''); ")

    def discount_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute(
                "insert into public.discount select (SELECT MAX(id)+1 FROM public.discount), "
                "FLOOR(RANDOM()*(100000-1)+1),"
                "FLOOR(RANDOM()*(100000-1)+1); ")

    def product_discount_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute(
                "insert into public.product_discount select (SELECT MAX(id)+1 FROM public.product_discount), "
                "(SELECT id FROM public.product LIMIT 1 OFFSET "
                "(round(random() *((SELECT COUNT(id) FROM public.product)-1)))), "
                "(SELECT id FROM public.discount LIMIT 1 OFFSET "
                "(round(random() *((SELECT COUNT(id) FROM public.discount)-1))));")

    def search_data_two_tables(self):
        return self.session.query(Shop).select_from(Discount) \
            .filter(and_(
            Shop.id <= 5,
            Discount.percent >= 20
        )).all()

    def search_data_three_tables(self):
        return self.session.query(Shop)\
            .select_from(Product_discount, Discount)\
            .filter(and_(
            Shop.id >= 5,
            Discount.percent <= 20,
            Product_discount.id >= 1
            ))\
            .all()

    def search_data_all_tables(self):
        return self.session.query(Shop) \
            .select_from(Product_discount, Discount, Product) \
            .filter(and_(
            Shop.id <= 2,
            Discount.percent <= 5,
            Product_discount.id <= 2,
            Product.id >= 4
            )) \
            .all()
