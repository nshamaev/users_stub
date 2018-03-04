import yaml
from pymongo import MongoClient

client = MongoClient('db')
users_db = client.users


def insert_users(db=users_db):
    with open("users.yml") as f:
        data = yaml.load(f)
        users = data.get('users', {})
        db.users.insert_many(users)


if __name__ == '__main__':
    insert_users()