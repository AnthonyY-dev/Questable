
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
collection_id = '683684a5003cc0ba234e' # Replace with your collection ID


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

    databases.create_document(
            database_id=database_id,
            collection_id=collection_id,
            document_id=ID.unique(), # Generates a unique ID for the document
            data=document_data
        )