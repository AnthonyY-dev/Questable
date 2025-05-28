from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
import os

isDevMode = os.getenv("devMode")


appWriteClient = Client()
if isDevMode=="0":
    appWriteClient.set_endpoint('https://fra.cloud.appwrite.io/v1') # Re  place with your Appwrite endpoint
    appWriteClient.set_project('68353a7b0002defacf67') # Replace with your project ID
    appWriteClient.set_key(os.getenv("prodAppwriteKey")) # Replace with your secret API key
elif isDevMode=="1":
    appWriteClient.set_endpoint('https://fra.cloud.appwrite.io/v1') # Re  place with your Appwrite endpoint
    appWriteClient.set_project('68353af3001e33714650') # Replace with your project ID
    appWriteClient.set_key(os.getenv("devAppwriteKey")) # Replace with your secret API key
databases = Databases(appWriteClient)

database_id = 'YOUR_DATABASE_ID' # Replace with your database ID
collection_id = 'YOUR_COLLECTION_ID' # Replace with your collection ID
document_data = {
    'attribute1': 'value1',
    'attribute2': 'value2'
    # Add more attributes as needed
}

result = databases.create_document(
        database_id=database_id,
        collection_id=collection_id,
        document_id=ID.unique(), # Generates a unique ID for the document
        data=document_data
    )

def addQuest(name: str, description: str, difficulty: int, xp_awarded: int, image: str | None):
    """
    @TODO
    """