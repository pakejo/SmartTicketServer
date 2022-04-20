from utils import get_db_handle, get_collection_handle
db_handle, mongo_client = get_db_handle()
collection_handle = get_collection_handle(db_handle, "sample_airbnb")