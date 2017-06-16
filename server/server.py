from flask import Flask
from flask_restful import Api
import views

app = Flask(__name__)
api = Api(app)

# Add urls
api.add_resource(views.ChatMessageAPIView, '/', '/chat_messages')

if __name__ == '__main__':
    app.run(debug=True)
