from flask import Flask
from flask_restful import Api
import views

app = Flask(__name__)
api = Api(app)

# Add index template
app.add_url_rule('/', 'index', views.IndexTemplate)

# Add API urls
api.add_resource(views.ChatMessageAPIView, '/', '/messages')
api.add_resource(views.ChatAPIView, '/', '/chats')


if __name__ == '__main__':
    app.run(debug=True)
