import os
import pathlib

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from cassandra.cqlengine.connection import register_connection, set_default_connection
from dotenv import load_dotenv


load_dotenv()
ASTRA_DB_CLIENT_ID = os.environ.get("ASTRA_DB_CLIENT_ID")
ASTRA_DB_CLIENT_SECRET = os.environ.get("ASTRA_DB_CLIENT_SECRET")

BASE_DIR = pathlib.Path(__file__).parent
CLUSTER_BUNDLE = str(BASE_DIR / "ignored" / "connect.zip")


def get_cluster():
    cloud_config = {
        'secure_connect_bundle': CLUSTER_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    return cluster


def get_session():
    cluster = get_cluster()
    session = cluster.connect()
    register_connection(str(session), session=session)
    set_default_connection(str(session))
    return session
