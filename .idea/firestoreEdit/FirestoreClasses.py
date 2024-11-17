import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Admin SDK 초기화
cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

class FirestoreCollection:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.collection = db.collection(collection_name)

    def user_exists(self, user):
        docs = self.collection.where('user', '==', user).stream()
        return any(docs)

    def to_dict(self, document):
        return document.to_dict()

    def from_dict(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def create(self, data):
        user = data.get('user')
        if self.user_exists(user):
            print(f"{self.collection_name} entry for this user already exists!")
            return None
        doc_ref = self.collection.add(data)
        print(f"{self.collection_name} document created successfully")
        return doc_ref

    def read(self, user):
        docs = self.collection.where('user', '==', user).stream()
        results = []
        for doc in docs:
            obj = self.__class__(self.collection_name)
            obj.from_dict(self.to_dict(doc))
            results.append(obj)
        return results

    def update(self, user, updates):
        docs = self.collection.where('user', '==', user).stream()
        for doc in docs:
            self.collection.document(doc.id).update(updates)
            print(f"{self.collection_name} document updated successfully")

    def delete(self, user):
        docs = self.collection.where('user', '==', user).stream()
        for doc in docs:
            self.collection.document(doc.id).delete()
            print(f"{self.collection_name} document deleted successfully")

# User 컬렉션 클래스
class UserCollection(FirestoreCollection):
    def __init__(self, callerID=None, user=None):
        super().__init__('user')
        self.callerID = callerID
        self.user = user

# AI_Image 컬렉션 클래스
class AIImageCollection(FirestoreCollection):
    def __init__(self, date=None, imagePath=None, user=None):
        super().__init__('AI_Image')
        self.date = date
        self.imagePath = imagePath
        self.user = user

# Image 컬렉션 클래스
class ImageCollection(FirestoreCollection):
    def __init__(self, date=None, imagePath=None, user=None):
        super().__init__('Image')
        self.date = date
        self.imagePath = imagePath
        self.user = user

# lastestImage 컬렉션 클래스
class LastestImageCollection(FirestoreCollection):
    def __init__(self, imagePathArray=None, user=None):
        super().__init__('lastestImage')
        self.imagePathArray = imagePathArray if imagePathArray else []
        self.user = user

    def trim_lastest_image_array(self, user):
        docs = self.collection.where('user', '==', user).stream()
        for doc in docs:
            data = self.to_dict(doc)
            if len(data['imagePathArray']) > 10:
                trimmed_array = data['imagePathArray'][1:]  # Remove the oldest element
                self.collection.document(doc.id).update({'imagePathArray': trimmed_array})
                print("Trimmed imagePathArray for user", user)

# lastest_contact 컬렉션 클래스
class LastestContactCollection(FirestoreCollection):
    def __init__(self, contactArray=None, user=None):
        super().__init__('lastest_contact')
        self.contactArray = contactArray if contactArray else []
        self.user = user

    def trim_lastest_contact_array(self, user):
        docs = self.collection.where('user', '==', user).stream()
        for doc in docs:
            data = self.to_dict(doc)
            if len(data['contactArray']) > 10:
                trimmed_array = data['contactArray'][1:]  # Remove the oldest element
                self.collection.document(doc.id).update({'contactArray': trimmed_array})
                print("Trimmed contactArray for user", user)

# lastest_AI_image 컬렉션 클래스

class LastestAIImageCollection(FirestoreCollection):
    def __init__(self, AI_image_array=None, user=None):
        super().__init__('lastest_AI_image')
        self.AI_image_array = AI_image_array if AI_image_array else []
        self.user = user

    def trim_lastest_AI_image_array(self, user):
        docs = self.collection.where('user', '==', user).stream()
        for doc in docs:
            data = self.to_dict(doc)
            if len(data['AI_image_array']) > 10:
                trimmed_array = data['AI_image_array'][1:]  # Remove the oldest element
                self.collection.document(doc.id).update({'AI_image_array': trimmed_array})
                print("Trimmed AI_image_array for user", user)

#lastestmessage 컬렉션 클래스
class LastestMessageCollection(FirestoreCollection):
    def __init__(self, lastestMessageArray=None, user=None):
        super().__init__('lastestMessage')
        self.lastestMessageArray = lastestMessageArray if lastestMessageArray else []
        self.user = user

    def trim_lastest_message_array(self, user):
        docs = self.collection.where('user', '==', user).stream()
        for doc in docs:
            data = self.to_dict(doc)
            if len(data['lastestMessageArray']) > 10:
                trimmed_array = data['lastestMessageArray'][1:]  # Remove the oldest element
                self.collection.document(doc.id).update({'lastestMessageArray': trimmed_array})
                print("Trimmed lastestMessageArray for user", user)

# message 컬렉션 클래스
class MessageCollection(FirestoreCollection):
    def __init__(self, context=None, date=None, subject=None, user=None):
        super().__init__('message')
        self.context = context
        self.date = date
        self.subject = subject
        self.user = user
