
from appwrite.id import ID
import os

isDevMode = os.getenv("devMode")
databases = None
appWriteHandler = None

def init(hndlr, dbs):
   global databases
   databases = dbs
   appWriteHandler = hndlr
   print("\033[0;32mAppwrite Initialized!\x1b[0m")

database_id = '6836849f002e091eb88a' # Replace with your database ID
quest_collection_id = '683684a5003cc0ba234e' # Replace with your collection ID


def addQuest(name: str, description: str, difficulty: int, xp_awarded: int, image_url: str | None = None):
    """
    @TODO
    """

    document_data = {
    'name': name,
    'description': description,
    'difficulty': difficulty,
    'xp_awarded': xp_awarded,
    'image_url': image_url
    # Add more attributes as needed
    }
    id = ID.unique()
    databases.create_document(
            database_id=database_id,
            collection_id=quest_collection_id,
            document_id=id, # Generates a unique ID for the document
            data=document_data
        )
    return id

def getQuestById(id: str):
    try:
        result = databases.get_document(
        database_id = database_id,
        collection_id = quest_collection_id,
        document_id = id,
        queries = [] 
        )
        return result
    except Exception as e:
        if str(e) == "Document with the requested ID could not be found.":
            return 404
    