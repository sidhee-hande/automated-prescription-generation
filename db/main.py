from azure.cosmos.aio import CosmosClient as cosmos_client
from azure.cosmos import PartitionKey, exceptions
import asyncio
import patients
from process_text import process_text
from speech_recognition import begin_recognizing

# <add_uri_and_key>
endpoint = "https://sadman123.documents.azure.com:443"
key = "Mn6etXvytGjBnqZ2ItEIxyzg7Kvn5gcd4oJJ8eBzyjCa8Es1WDO8KOuXvfeHTE1wFYntH1nhdICGOtWtLVrYXQ=="


# <define_database_and_container_name>
database_name = 'prescriptions'
container_name = 'prescriptions'


# get DB or create if it doesn't exist
async def get_or_create_db(client, database_name):
    try:
        database_obj = client.get_database_client(database_name)
        await database_obj.read()
        return database_obj
    except exceptions.CosmosResourceNotFoundError:
        print("getting database")
        return await client.create_database(database_name)


# get container or create if it doesn't exist
async def get_or_create_container(database_obj, container_name):
    try:
        todo_items_container = database_obj.get_container_client(
            container_name)
        await todo_items_container.read()
        return todo_items_container
    except exceptions.CosmosResourceNotFoundError:
        print("Creating container with lastName as partition key")
        return await database_obj.create_container(
            id=container_name,
            partition_key=PartitionKey(path="/lastName"),
            offer_throughput=400)
    except exceptions.CosmosHttpResponseError:
        raise


# add stuff to the container
async def populate_container_items(container_obj, items_to_create):
    # Add items to the container
    family_items_to_create = items_to_create
    # <create_item>
    for family_item in family_items_to_create:
        inserted_item = await container_obj.create_item(body=family_item)


# <method_read_items>
async def read_items(container_obj, items_to_read):
    # Read items (key value lookups by partition key and id, aka point reads)
    # <read_item>
    for family in items_to_read:
        item_response = await container_obj.read_item(item=family['id'], partition_key=family['lastName'])
        request_charge = container_obj.client_connection.last_response_headers[
            'x-ms-request-charge']
        print('Read item with id {0}. Operation consumed {1} request units'.format(
            item_response['id'], (request_charge)))

# query items with sql queries


async def query_items(container_obj, query_text):
    # enable_cross_partition_query should be set to True as the container is partitioned
    # In this case, we do have to await the asynchronous iterator object since logic
    # within the query_items() method makes network calls to verify the partition key
    # definition in the container
    # <query_items>
    query_items_response = container_obj.query_items(
        query=query_text,
        enable_cross_partition_query=True
    )
    request_charge = container_obj.client_connection.last_response_headers[
        'x-ms-request-charge']
    items = [item async for item in query_items_response]
    print(items)
    print('Query returned {0} items. Operation consumed {1} request units'.format(
        len(items), request_charge))
    # </query_items>
    return items


# runs everything
async def run_sample():
    # <create_cosmos_client>
    async with cosmos_client(endpoint, credential=key) as client:
        # </create_cosmos_client>
        try:
            # create a database
            database_obj = await get_or_create_db(client, database_name)
            # create a container
            container_obj = await get_or_create_container(database_obj, container_name)
            # generate some family items to test create, read, delete operations
            items_to_create = [
                patients.get_smith_item(), patients.get_johnson_item()]
            # populate the family items in container
            await populate_container_items(container_obj, items_to_create)

            query = "SELECT * FROM c WHERE c.lastName IN ('Smith', 'Andersen')"
            await query_items(container_obj, query)
        except exceptions.CosmosHttpResponseError as e:
            print('\nrun_sample has caught an error. {0}'.format(e.message))
        finally:
            print("\nQuickstart complete")


async def send_data(data):
    async with cosmos_client(endpoint, credential=key) as client:
        # </create_cosmos_client>
        try:
            database_obj = await get_or_create_db(client, database_name)
            container_obj = await get_or_create_container(database_obj, container_name)
            # generate some family items to test create, read, delete operations
            await populate_container_items(container_obj, data)
        except exceptions.CosmosHttpResponseError as e:
            print('\nsend data has caught an error. {0}'.format(e.message))


async def get_data(query):
    async with cosmos_client(endpoint, credential=key) as client:
        # </create_cosmos_client>
        try:
            database_obj = await get_or_create_db(client, database_name)
            container_obj = await get_or_create_container(database_obj, container_name)
            # generate some family items to test create, read, delete operations
            items = await query_items(container_obj, query)
        except exceptions.CosmosHttpResponseError as e:
            print('\nsend data has caught an error. {0}'.format(e.message))

# <python_main>
# if __name__ == "__main__":
    #loop = asyncio.get_event_loop()
    # loop.run_until_complete(run_sample())


async def start_process():
    text = ""
    with open('convo.txt', 'r') as f:
        text = f.read()
    processed_text = process_text(text)

    await send_data([processed_text])


# <python_main>
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_process())
