from flask import Flask
from flask_restful import Api
import views

app = Flask(__name__)
api = Api(app)

# Add environmental variable


# Add urls
api.add_resource(views.ChatMessageAPIView, '/', '/messages')
api.add_resource(views.ChatAPIView, '/', '/chats')

if __name__ == '__main__':
    app.run(debug=True)
