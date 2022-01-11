from playhouse.migrate import *
my_db = SqliteDatabase('database.db')
migrator = SqliteMigrator(my_db)
migrate(migrator.add_column('device', 'ip_addr', CharField(null=True)))
