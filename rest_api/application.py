from flask import Flask
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)

hostURL = "0.0.0.0"
hostPort = 1337
apiRoute = '/hello'

def getAPIInfo():
    return (hostURL, hostPort)

@api.route(apiRoute)
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'} 

if __name__ == '__main__':
    app.run(host=hostURL, port=hostPort, debug=True)