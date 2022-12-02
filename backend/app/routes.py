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
    family_items_to_create = items_to_create
    print(items_to_create)
    # <create_item>
    for family_item in family_items_to_create:
        inserted_item = await container_obj.create_item(body=family_item)
        print("Inserted item for Item Id: %s" %
              ( inserted_item['id']))

async def query_items(container_obj, query_text):
    # enable_cross_partition_query should be set to True as the container is partitioned
    # In this case, we do have to await the asynchronous iterator object since logic
    # within the query_items() method makes network calls to verify the partition key
    # definition in the container
    # <query_items>
    
        
    query_items_response = container_obj.query_items(query=query_text,
        enable_cross_partition_query=True)

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
    return items
    # </query_items>


async def add_data(endpoint, key, database_name, container_name, data):
    message = ""
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
            items_to_create = [ data]
           
            await populate_container_items(container_obj, items_to_create)

            # query = "SELECT * FROM c WHERE c.lastName IN ('Smith', 'Andersen')"
            # await query_items(container_obj, query)
            print("Data saved successfully!")
            message = "Data saved successfully!"
        except exceptions.CosmosHttpResponseError as e:
            print('\nadd_data has caught an error. {0}'.format(e.message))
            message = '\nadd_data has caught an error. {0}'.format(e.message)
        finally:
            print("\nQuickstart complete")
           
            return message

async def get_data(endpoint, key, database_name, container_name, query):
    items = []
    #<create_cosmos_client>
    async with cosmos_client(endpoint, key) as client:
        # </create_cosmos_client>
        try:
            # create a database
            database_obj = await get_or_create_db(client, database_name)
            # create a container
            container_obj = await get_or_create_container(
                database_obj, container_name)

            
            items = await query_items(container_obj, query)
            print(items)
        except exceptions.CosmosHttpResponseError as e:
            print('\nadd_data has caught an error. {0}'.format(e.message))
            data = '\nadd_data has caught an error. {0}'.format(e.message)
            return data
        finally:
            print("\nQuickstart complete")
            
            return items
    _



@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/api/getpatientdata', methods=['GET'])
@route_cors(allow_origin="*")
async def get_patient_data():
    container_name = "patients"
    query = "SELECT * FROM c"
    message = await get_data(endpoint, key, database_name, container_name, query)
    print(message)

    return message

@app.route('/api/getprescriptiondata', methods=['GET'])
@route_cors(allow_origin="*")
async def get_prescription_data():
    container_name = "prescriptions"
    query = "SELECT * FROM c"
    message = await get_data(endpoint, key, database_name, container_name, query)
    print(message)

    return message

@app.route('/api/searchpatientdata', methods=['POST'])
@route_cors(allow_origin="*")
async def search_patient():
    data = await request.get_json()
    patient_email =  data ["email"]

    container_name = "patients"
    
    query = "SELECT * FROM c WHERE c.email='" + patient_email +"'"
    message = await get_data(endpoint, key, database_name, container_name, query)
    print(message)
    
    return message
@app.route('/api/searchprescriptiondata', methods=['POST'])
@route_cors(allow_origin="*")
async def search_prescription_data():
    data = await request.get_json()
    patient_email =  data ["email"]

    container_name = "prescriptions"
    
    query = "SELECT * FROM c WHERE c.email='" + patient_email +"'"
    message = await get_data(endpoint, key, database_name, container_name, query)
    print(message)
    
    return message

@app.route('/api/addpatient', methods=['POST'])
@route_cors(allow_origin="*")
async def add_patient_data():
    data = await request.get_json()
    patient =  data ["patient"]
    print(patient)
    patient ["id"] = str(uuid.uuid4())
    print(patient)
    #add doctor's id in the patient dictionary
    container_name = "patients"
    message = await add_data(endpoint, key, database_name, container_name, patient)

    return message

@app.route('/api/saveprescription', methods=['POST'])
@route_cors(allow_origin="*")
async def save_data():
   # save prescription in database
    data = await request.get_json()
    prescription =  data["prescription"][0]
    print(prescription)
    prescription["prescription_id"] = str(uuid.uuid4())
    print(prescription)
    #container_obj = ""
    container_name = 'prescriptions'
    message = await add_data(endpoint, key, database_name, container_name, prescription)
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
