import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify

# Firebase Admin SDK 초기화
cred = credentials.Certificate("flightinfo-46895-firebase-adminsdk-c5i7h-fd4b966360")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

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

# User 컬렉션 API
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    user_collection = UserCollection()
    if user_collection.user_exists(data['user']):
        return jsonify({"message": "User already exists!"}), 400
    user_collection.create(data)
    return jsonify({"message": "User created successfully"}), 201

@app.route('/get_user/<user>', methods=['GET'])
def get_user(user):
    user_collection = UserCollection()
    result = user_collection.read(user)
    return jsonify([obj.__dict__ for obj in result]), 200

# AI_Image 컬렉션 API
@app.route('/create_ai_image', methods=['POST'])
def create_ai_image():
    data = request.json
    ai_image_collection = AIImageCollection()
    if ai_image_collection.user_exists(data['user']):
        return jsonify({"message": "AI_Image entry for this user already exists!"}), 400
    ai_image_collection.create(data)
    return jsonify({"message": "AI_Image created successfully"}), 201

@app.route('/get_ai_image/<user>', methods=['GET'])
def get_ai_image(user):
    ai_image_collection = AIImageCollection()
    result = ai_image_collection.read(user)
    return jsonify([obj.__dict__ for obj in result]), 200

# Image 컬렉션 API
@app.route('/create_image', methods=['POST'])
def create_image():
    data = request.json
    image_collection = ImageCollection()
    if image_collection.user_exists(data['user']):
        return jsonify({"message": "Image entry for this user already exists!"}), 400
    image_collection.create(data)
    return jsonify({"message": "Image created successfully"}), 201

@app.route('/get_image/<user>', methods=['GET'])
def get_image(user):
    image_collection = ImageCollection()
    result = image_collection.read(user)
    return jsonify([obj.__dict__ for obj in result]), 200

# lastestImage 컬렉션 API
@app.route('/create_lastest_image', methods=['POST'])
def create_lastest_image():
    data = request.json
    lastest_image_collection = LastestImageCollection()
    if lastest_image_collection.user_exists(data['user']):
        return jsonify({"message": "lastestImage entry for this user already exists!"}), 400
    lastest_image_collection.create(data)
    return jsonify({"message": "lastestImage created successfully"}), 201

@app.route('/get_lastest_image/<user>', methods=['GET'])
def get_lastest_image(user):
    lastest_image_collection = LastestImageCollection()
    result = lastest_image_collection.read(user)
    return jsonify([obj.__dict__ for obj in result]), 200

@app.route('/trim_lastest_image/<user>', methods=['POST'])
def trim_lastest_image(user):
    lastest_image_collection = LastestImageCollection()
    lastest_image_collection.trim_lastest_image_array(user)
    return jsonify({"message": f"Trimmed imagePathArray for user {user}"}), 200

# lastest_contact 컬렉션 API
@app.route('/create_lastest_contact', methods=['POST'])
def create_lastest_contact():
    data = request.json
    lastest_contact_collection = LastestContactCollection()
    if lastest_contact_collection.user_exists(data['user']):
        return jsonify({"message": "lastest_contact entry for this user already exists!"}), 400
    lastest_contact_collection.create(data)
    return jsonify({"message": "lastest_contact created successfully"}), 201

@app.route('/get_lastest_contact/<user>', methods=['GET'])
def get_lastest_contact(user):
    lastest_contact_collection = LastestContactCollection()
    result = lastest_contact_collection.read(user)
    return jsonify([obj.__dict__ for obj in result]), 200

@app.route('/trim_lastest_contact/<user>', methods=['POST'])
def trim_lastest_contact(user):
    lastest_contact_collection = LastestContactCollection()
    lastest_contact_collection.trim_lastest_contact_array(user)
    return jsonify({"message": f"Trimmed contactArray for user {user}"}), 200

# message 컬렉션 API
@app.route('/create_message', methods=['POST'])
def create_message():
    data = request.json
    message_collection = MessageCollection()
    if message_collection.user_exists(data['user']):
        return jsonify({"message": "Message entry for this user already exists!"}), 400
    message_collection.create(data)
    return jsonify({"message": "Message created successfully"}), 201


@app.route('/get_message/<user>', methods=['GET'])
def get_message(user):
    message_collection = MessageCollection()
    result = message_collection.read(user)
    return jsonify([obj.__dict__ for obj in result]), 200

# lastest_AI_image 컬렉션 클래스 및 API
class LastestAIImageCollection(FirestoreCollection):
    def __init__(self, AI_image_array=None, user=None):
        super().__init__('lastest_AI_image')
        self.AI_image_array = AI_image_array if AI_image_array else []
        self.user = user

    def trim_AI_image_array(self, user):
        docs = self.collection.where('user', '==', user).stream()
        for doc in docs:
            data = self.to_dict(doc)
            if len(data['AI_image_array']) > 20:
                trimmed_array = data['AI_image_array'][1:]  # Remove the oldest element
                self.collection.document(doc.id).update({'AI_image_array': trimmed_array})
                print("Trimmed AI_image_array for user", user)

@app.route('/create_lastest_ai_image', methods=['POST'])
def create_lastest_ai_image():
    data = request.json
    lastest_ai_image_collection = LastestAIImageCollection()
    if lastest_ai_image_collection.user_exists(data['user']):
        return jsonify({"message": "lastest_AI_image entry for this user already exists!"}), 400
    lastest_ai_image_collection.create(data)
    return jsonify({"message": "lastest_AI_image created successfully"}), 201

@app.route('/get_lastest_ai_image/<user>', methods=['GET'])
def get_lastest_ai_image(user):
    lastest_ai_image_collection = LastestAIImageCollection()
    result = lastest_ai_image_collection.read(user)
    return jsonify([obj.__dict__ for obj in result]), 200

@app.route('/trim_lastest_ai_image/<user>', methods=['POST'])
def trim_lastest_ai_image(user):
    lastest_ai_image_collection = LastestAIImageCollection()
    lastest_ai_image_collection.trim_AI_image_array(user)
    return jsonify({"message": f"Trimmed AI_image_array for user {user}"}), 200



@app.route('/create_lastest_ai_image', methods=['POST'])
def create_lastest_ai_image():
    data = request.json
    lastest_ai_image_collection = LastestAIImageCollection()
    if lastest_ai_image_collection.user_exists(data['user']):
        return jsonify({"message": "lastest_AI_image entry for this user already exists!"}), 400
    lastest_ai_image_collection.create(data)
    return jsonify({"message": "lastest_AI_image created successfully"}), 201

@app.route('/get_lastest_ai_image/<user>', methods=['GET'])
def get_lastest_ai_image(user):
    lastest_ai_image_collection = LastestAIImageCollection()
    result = lastest_ai_image_collection.read(user)
    return jsonify([obj.__dict__ for obj in result]), 200

@app.route('/trim_lastest_ai_image/<user>', methods=['POST'])
def trim_lastest_ai_image(user):
    lastest_ai_image_collection = LastestAIImageCollection()
    lastest_ai_image_collection.trim_lastest_AI_image_array(user)
    return jsonify({"message": f"Trimmed AI_image_array for user {user}"}), 200



# lastestMessage 컬렉션 API
@app.route('/create_lastest_message', methods=['POST'])
def create_lastest_message():
    data = request.json
    lastest_message_collection = LastestMessageCollection()
    if lastest_message_collection.user_exists(data['user']):
        return jsonify({"message": "lastestMessage entry for this user already exists!"}), 400
    lastest_message_collection.create(data)
    return jsonify({"message": "lastestMessage created successfully"}), 201

@app.route('/get_lastest_message/<user>', methods=['GET'])
def get_lastest_message(user):
    lastest_message_collection = LastestMessageCollection()
    result = lastest_message_collection.read(user)
    return jsonify([obj.__dict__ for obj in result]), 200

@app.route('/trim_lastest_message/<user>', methods=['POST'])
def trim_lastest_message(user):
    lastest_message_collection = LastestMessageCollection()
    lastest_message_collection.trim_lastest_message_array(user)
    return jsonify({"message": f"Trimmed lastestMessageArray for user {user}"}), 200

# @app.route('/update_lastest_message/<user>', methods=['PUT'])
# def update_lastest_message(user):
#     data = request.json
#     lastest_message_collection = LastestMessageCollection()
#     if not lastest_message_collection.user_exists(user):
#         return jsonify({"message": "lastestMessage entry for this user does not exist!"}), 404
#     lastest_message_collection.update(user, data)
#     return jsonify({"message": "lastestMessage updated successfully"}), 200
#
# @app.route('/delete_lastest_message/<user>', methods=['DELETE'])
# def delete_lastest_message(user):
#     lastest_message_collection = LastestMessageCollection()
#     if not lastest_message_collection.user_exists(user):
#         return jsonify({"message": "lastestMessage entry for this user does not exist!"}), 404
#     lastest_message_collection.delete(user)
#     return jsonify({"message": "lastestMessage deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
