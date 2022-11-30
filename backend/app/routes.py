# from quart_cors import CORS, cross_origin
from quart_cors import route_cors
from app import app
from datetime import date
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from click import DateTime
from config import textanalyticskey
from quart import request
from azure.cosmos.aio import CosmosClient as cosmos_client
from azure.cosmos import PartitionKey, exceptions
import asyncio
import uuid
endpoint = "https://sadman123.documents.azure.com:443"
key = "Mn6etXvytGjBnqZ2ItEIxyzg7Kvn5gcd4oJJ8eBzyjCa8Es1WDO8KOuXvfeHTE1wFYntH1nhdICGOtWtLVrYXQ=="
    # <define_database_and_container_name>
database_name = 'prescriptions'


# get DB or create if it doesn't exist
async def get_or_create_db(client, database_name):
    print("FN 1")
    try:
        database_obj = client.get_database_client(database_name)
        await database_obj.read()
        print( "FN 1 Database",database_obj)
        return database_obj
    except exceptions.CosmosResourceNotFoundError:
        print("getting database")
        return client.create_database(database_name)


# get container or create if it doesn't exist
async def get_or_create_container(database_obj, container_name):
    print("FN 2")
    try:
        todo_items_container = database_obj.get_container_client(
            container_name)
        await todo_items_container.read()
        print( "FN 2 Container", todo_items_container)
        return todo_items_container
    except exceptions.CosmosResourceNotFoundError:
        print("Creating container with lastName as partition key")
        return database_obj.create_container(
            id=container_name,
            partition_key=PartitionKey(path="/lastName"),
            offer_throughput=400)
    except exceptions.CosmosHttpResponseError:
        raise


# add stuff to the container
async def populate_container_items(container_obj, items_to_create):
    # Add items to the container
    print("FN 3")
    # items_to_create = [ {
    #     'id': 'fhsbfksf' + str(uuid.uuid4()),
    #     'lastName': 'Johnson',
    #     'district': None,
    #     'registered': False
    # }]
    family_items_to_create = items_to_create
    # <create_item>
    for family_item in family_items_to_create:
        inserted_item = await container_obj.create_item(body=family_item)
        print("Inserted item for Item Id: %s" %
              ( inserted_item['id']))


async def run_sample(endpoint, key, database_name, container_name, prescription):
    data = " "
    
    #<create_cosmos_client>
    async with cosmos_client(endpoint, key) as client:
        # </create_cosmos_client>
        try:
            # create a database
            database_obj = await get_or_create_db(client, database_name)
            # create a container
            container_obj = await get_or_create_container(
                database_obj, container_name)
            # # generate some family items to test create, read, delete operations
            items_to_create = [ prescription]
            await populate_container_items(container_obj, items_to_create)

            # query = "SELECT * FROM c WHERE c.lastName IN ('Smith', 'Andersen')"
            # await query_items(container_obj, query)
            print("Data saved successfully!")
        except exceptions.CosmosHttpResponseError as e:
            print('\nrun_sample has caught an error. {0}'.format(e.message))
            data = '\nrun_sample has caught an error. {0}'.format(e.message)
        finally:
            print("\nQuickstart complete")
            return data 
            \

# if __name__ == "__main__":

#     # <add_uri_and_key>
#     endpoint = "https://sadman123.documents.azure.com:443"
#     key = "Mn6etXvytGjBnqZ2ItEIxyzg7Kvn5gcd4oJJ8eBzyjCa8Es1WDO8KOuXvfeHTE1wFYntH1nhdICGOtWtLVrYXQ=="
#     # <define_database_and_container_name>
#     database_name = 'prescriptions'
#     container_name = 'meetings'
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(run_sample(
#         endpoint, key, database_name, container_name))


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/api/getdata', methods=['GET'])
@route_cors(allow_origin="*")
def get_todos():

    return "Get Request API Check"

async def dummy_data():
    return " dhh"

@app.route('/api/saveprescription', methods=['POST'])
@route_cors(allow_origin="*")
async def save_data():
   # save prescription in database
    data = await request.get_json()
    prescription =  data["prescription"]
    prescription["id"] = str(uuid.uuid4())
    print(prescription)
    #container_obj = ""
    container_name = 'prescriptions'
    message = await run_sample(endpoint, key, database_name, container_name, prescription)
    return message


@app.route('/api/generateprescription', methods=['POST'])
@route_cors(allow_origin="*")
async def get_prescription():

    credential = AzureKeyCredential(textanalyticskey)
    text_analytics_client = TextAnalyticsClient(
        endpoint="https://automaticprescriptiongenerator.cognitiveservices.azure.com/", credential=credential)

    # read the transcript from database
    data =  await request.get_json()
    print(data)
    documents = [data["transcript"]]
    print(documents)

    patientname = ''
    age = ''
    todaysdate = ''
    symptoms = []
    medicines = []
    dosageofmedication = []
    frequencyofmedication = []
    relations = []
    diagnosis = []

    response = text_analytics_client.recognize_entities(
        documents, language="en")
    result = [doc for doc in response if not doc.is_error]

    for doc in result:
        for entity in doc.entities:
            print(f"Entity: {entity.text}")
            print(f"...Category: {entity.category}")
            if entity.category == 'Person':
                patientname = entity.text
                break

    poller = text_analytics_client.begin_analyze_healthcare_entities(documents)
    result = poller.result()

    docs = [doc for doc in result if not doc.is_error]

    print("Results of Healthcare Entities Analysis:")
    for idx, doc in enumerate(docs):
        for entity in doc.entities:
            print(f"Entity: {entity.text}")
            print(f"...Normalized Text: {entity.normalized_text}")
            print(f"...Category: {entity.category}")
            print(f"...Subcategory: {entity.subcategory}")

            if entity.category == 'SymptomOrSign':
                print(f"Entity: {entity.text}")
                symptoms.append(entity.text)
            if entity.category == 'Age':
                age = entity.text
            if entity.category == 'Diagnosis':
                print(f"Entity: {entity.text}")
                diagnosis.append(entity.text)
            if entity.category == 'MedicationName':
                print(f"Entity: {entity.text}")
                medicines.append(entity.text)

        for relation in doc.entity_relations:
            print(
                f"Relation of type: {relation.relation_type} has the following roles")
            if relation.relation_type == "DosageOfMedication":
                st = ''
                for role in relation.roles:
                    st = st+role.entity.text+" "
                dosageofmedication.append(st)
            elif relation.relation_type == "FrequencyOfMedication":
                st = ''
                for role in relation.roles:
                    st = st+role.entity.text+" "
                frequencyofmedication.append(st)
            else:
                for role in relation.roles:

                    print(f"'{role.name}': '{role.entity.text}'")
                    relations.append(f"'{role.name}': '{role.entity.text}'")

        print("------------------------------------------")

        todaysdate = date.today()

        print(patientname)
        print(age)
        print(todaysdate)
        print(symptoms)
        print(diagnosis)
        print(medicines)
        print(dosageofmedication)
        print(frequencyofmedication)
        print(relations)

        symptomsoutput = " ".join(symptoms)
        diagnosisoutput = " ".join(diagnosis)
        medicinesoutput = " ".join(medicines)
        dosageofmedicationoutput = " ".join(dosageofmedication)
        frequencyofmedicationoutput = " ".join(frequencyofmedication)

        prescription = dict()
        patientid = 1
        prescription[patientid] = {
            "name": patientname,
            "age": age,
            "date": todaysdate,
            "symptoms": symptomsoutput,
            "diagnosis": diagnosisoutput,
            "medicines": medicinesoutput,
            "dosageofmedication": dosageofmedicationoutput,
            "frequencyofmedication": frequencyofmedicationoutput,
            "edit": True

        }

        print(prescription)

        return prescription[patientid]
