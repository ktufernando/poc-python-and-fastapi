from peewee import *
from playhouse.db_url import connect
from config import DATABASE_URL

database = connect(DATABASE_URL)


class User(Model):
    username = CharField(max_length=50, unique=True)
    email = CharField(max_length=50, unique=True)

    def __str__(self):
        return self.username

    class Meta:
        database = database
        table_name = 'users'
