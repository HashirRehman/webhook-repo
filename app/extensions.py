from flask_pymongo import PyMongo

def init_mongo(app):
    mongo_uri = "mongodb+srv://hashir:postgres@webhook.qwbok.mongodb.net/webhooks?retryWrites=true&w=majority"
    app.config['MONGO_URI'] = mongo_uri
    mongo = PyMongo(app)
    app.db = mongo.db.github
    return mongo
