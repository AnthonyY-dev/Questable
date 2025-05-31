
from appwrite.id import ID
import os
from .utils import calculateLevel
from pprint import pprint

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
user_collection_id = '683a19cf0027a636c0d2'

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
        return 404
    
def markQuestAccepted(userId: int, questId: str):
    # get quest details
    
    questDetails = getQuestById(questId)
    
    if questDetails == 404:
        print(f'\x1b[91mERROR! A call to markQuestAccepted has been made, however the quest ID is invalid! Quest ID: {questId}\x1b[0m')
    
    
    # check if user is in db
    
    try:
        result = databases.get_document(
        database_id = database_id,
        collection_id = user_collection_id,
        document_id = str(userId),
        queries = [] 
        )
        # print(result)
        
        # user in db, add quest to him
        
        
        
        if questId in result['pendingQuests']:
            result['pendingQuests'].remove(questId)
        result['completedQuests'].append(questId)
        result['xp'] += questDetails['xp_awarded']
        result['level'] = calculateLevel(result['xp'])

        
        updateResult = databases.update_document(
            database_id=database_id,
            collection_id = user_collection_id,
            document_id=str(userId),
            data={
            'completedQuests': result['completedQuests'],
            'xp': result['xp'],
            'level': result['level'],
            'pendingQuests': result['pendingQuests']
        }
        )
        
    except Exception as e:
        # create user
        userData = {
            'completedQuests': [questId],
            'xp': 0,
            'level': calculateLevel(questDetails['xp_awarded']),
            'pendingQuests': []
        }

        databases.create_document(
            database_id=database_id,
            collection_id=user_collection_id,
            document_id=str(userId),
            data=userData
        )