from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from click import DateTime
from config import textanalyticskey

from datetime import date

from app import app
from flask_cors import CORS,cross_origin

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/api/getdata', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def get_todos():
   
    return "Get Request API Check"

@app.route('/api/startrecording', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def start_recording():
   
    return "Recording started"


@app.route('/api/generateprescription', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def get_prescription():
   
    credential = AzureKeyCredential(textanalyticskey)
    text_analytics_client = TextAnalyticsClient(endpoint="https://automaticprescriptiongenerator.cognitiveservices.azure.com/", credential=credential)
    
    #read the transcript from database
    documents = [""" Subject's name is Jeff Bezos. He is 45 years old. Subject is showing signs of chest pain, cough and fever.
I suspect it to be a case of Covid-19. 
Subject is advised to take 100mg of ibuprofen twice daily."""]


    patientname=''
    age=''
    todaysdate=''
    symptoms=[]
    medicines=[]
    dosageofmedication=[]
    frequencyofmedication=[]
    relations=[]
    diagnosis=[]

    response = text_analytics_client.recognize_entities(documents, language="en")
    result = [doc for doc in response if not doc.is_error]

    for doc in result:
        for entity in doc.entities:
            print(f"Entity: {entity.text}")
            print(f"...Category: {entity.category}")
            if entity.category=='Person':
                patientname=entity.text
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

            if entity.category=='SymptomOrSign':
                print(f"Entity: {entity.text}")
                symptoms.append(entity.text)
            if entity.category=='Age':
                age=entity.text
            if entity.category=='Diagnosis':
                print(f"Entity: {entity.text}")
                diagnosis.append(entity.text)
            if entity.category=='MedicationName':
                print(f"Entity: {entity.text}")
                medicines.append(entity.text)
           
        for relation in doc.entity_relations:
            print(f"Relation of type: {relation.relation_type} has the following roles")
            if relation.relation_type=="DosageOfMedication":
                st=''
                for role in relation.roles:
                    st=st+role.entity.text+" "
                dosageofmedication.append(st)
            elif relation.relation_type=="FrequencyOfMedication":
                st=''
                for role in relation.roles:
                    st=st+role.entity.text+" "
                frequencyofmedication.append(st)
            else:
                for role in relation.roles:
            
                    print(f"'{role.name}': '{role.entity.text}'")
                    relations.append(f"'{role.name}': '{role.entity.text}'")

        print("------------------------------------------")


        todaysdate=date.today()

        print(patientname)
        print(age)
        print(todaysdate)
        print(symptoms)
        print(diagnosis)
        print(medicines)
        print(dosageofmedication)
        print(frequencyofmedication)
        print(relations)

        prescription=dict()
        patientid=1
        prescription[patientid]= {
            "name": patientname,
            "age" : age, 
            "date" : todaysdate,
            "symptoms": symptoms,
            "diagnosis": diagnosis, 
            "medicines": medicines,
            "dosageofmedication": dosageofmedication,
            "frequencyofmedication": frequencyofmedication
        }

        print(prescription)



        return prescription