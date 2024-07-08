import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Stock, Sale, Shop
import json


SQLsystem = 'postgresql'
login = 'postgres'
password = '12345'
host = 'localhost'
port = 5432
db_name = "book_shop_db"
DSN = f'{SQLsystem}://{login}:{password}@{host}:{port}/{db_name}'
engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

with open('tests_data.json', 'r') as db:
    data = json.load(db)

for line in data:
    method = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[line['model']]
    session.add(method(id=line['pk'], **line.get('fields')))

session.commit()

def sale_list():
    search = input('Введите идентификатор или имя издателя: ')
    if search.isnumeric():
        results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
            .join(Publisher, Publisher.id == Book.id_publisher) \
            .join(Stock, Stock.id_book == Book.id) \
            .join(Shop, Shop.id == Stock.id_shop) \
            .join(Sale, Sale.id_stock == Stock.id) \
            .filter(Publisher.id == int(search)).all()
        for book, shop, price, date in results:
            print(f'{book: <40} | {shop: <10} | {price: <10} | {date.strftime("%Y-%m-%d")}')
    else:
        results = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale) \
            .join(Publisher, Publisher.id == Book.id_publisher) \
            .join(Stock, Stock.id_book == Book.id) \
            .join(Shop, Shop.id == Stock.id_shop) \
            .join(Sale, Sale.id_stock == Stock.id) \
            .filter(Publisher.name.like(f'%{search}%')).all()
        for book, shop, price, date in results:
            print(f'{book: <40} | {shop: <10} | {price: <10} | {date.strftime("%Y-%m-%d")}')

if __name__ == '__main__':
    sale_list()

session.close()



