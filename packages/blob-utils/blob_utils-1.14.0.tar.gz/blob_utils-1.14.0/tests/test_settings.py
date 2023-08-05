""" Tests settings
"""

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_NAME = "test"

MONGODB_URI = "mongodb://%s:%d/%s" % (MONGO_HOST, MONGO_PORT, MONGO_NAME)
