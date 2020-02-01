from pony import orm

# The main, single database used by this application.
#
# The database should be configured separately in a main function.
db = orm.Database()
