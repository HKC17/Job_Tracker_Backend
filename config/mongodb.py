"""
MongoDB connection utility using PyMongo.
This provides a singleton connection to MongoDB.
"""

from pymongo import MongoClient
from django.conf import settings


class MongoDB:
    """Singleton MongoDB connection class."""

    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self.connect()

    def connect(self):
        """Establish connection to MongoDB."""
        mongo_settings = settings.MONGODB_SETTINGS

        # Build connection string
        if mongo_settings['username'] and mongo_settings['password']:
            connection_string = (
                f"mongodb://{mongo_settings['username']}:{mongo_settings['password']}"
                f"@{mongo_settings['host']}:{mongo_settings['port']}/{mongo_settings['db_name']}"
            )
        else:
            connection_string = (
                f"mongodb://{mongo_settings['host']}:{mongo_settings['port']}"
            )

        try:
            self._client = MongoClient(connection_string)
            self._db = self._client[mongo_settings['db_name']]

            # Test connection
            self._client.admin.command('ping')
            print(f"✅ Connected to MongoDB: {mongo_settings['db_name']}")

        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {str(e)}")
            raise

    @property
    def db(self):
        """Get database instance."""
        if self._db is None:
            self.connect()
        return self._db

    @property
    def client(self):
        """Get client instance."""
        if self._client is None:
            self.connect()
        return self._client

    def get_collection(self, collection_name):
        """Get a specific collection."""
        return self.db[collection_name]

    def close(self):
        """Close MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("MongoDB connection closed.")


# Global MongoDB instance
mongodb = MongoDB()


# Helper functions for easy access
def get_db():
    """Get MongoDB database instance."""
    return mongodb.db


def get_collection(collection_name):
    """Get a MongoDB collection."""
    return mongodb.get_collection(collection_name)


def close_connection():
    """Close MongoDB connection."""
    mongodb.close()
