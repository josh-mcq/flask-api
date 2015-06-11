from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'josh':
        return 'flaskapi'
    return None



@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)

speeches = [
    {
        'id': 1,
        'topic': u'Fear of Public Speaking',
        'event': u'Toastmasters',
        'date': '2015-06-09'
    },
    {
        'id': 2,
        'topic': u'Some Technical Speech',
        'event': u'Toastmasters',
        'date': u'2015-07-08'
    }

]
speech_fields = {
	'topic': fields.String,
    'event': fields.String,
    'uri': fields.Url('speech'),
    'date': fields.String
}

class SpeechListAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('topic', type = str, required = True,
            help = 'No Topic Provided', location = 'json')
        self.reqparse.add_argument('event', type = str, required = True,
            help = 'No Event Provided', location = 'json')
        self.reqparse.add_argument('date', type = str, required = True,
            help = 'No Topic Provided', location = 'json')
        super(SpeechListAPI, self).__init__()

    def get(self):
        return {'speeches': [marshal(speech, speech_fields) for speech in speeches]}
        
    def post(self):
        args =  self.reqparse.parse_args()
        speech = {
            'id':speeches[-1]['id'] + 1,
            'topic':args['topic'],
            'event':args['event'],
            #'link':args['link'],
            'date':args['date']
        }
        speeches.append(speech)
        return {'speech': marshal(speech, speech_fields)}, 201

class SpeechAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('topic', type=str, location='json')
        self.reqparse.add_argument('event', type=str, location='json')
        self.reqparse.add_argument('data', type=str, location='json')
        super(SpeechAPI, self).__init__()

    def get(self, id):
        speech = [speech for speech in speeches if speech['id'] == id]
        if len(speech) == 0:
            abort(404)
        speech = speech[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                speech[k] = v
            return {'speech': marshal(speech, speech_fields)}

#api.add_resource(UserAPI, '/users/<int:id>', endpoint= 'user')
api.add_resource(SpeechListAPI, '/josh/api/v1.0/speeches', endpoint = 'speeches')
api.add_resource(SpeechAPI, '/josh/api/v1.0/speeches/<int:id>', endpoint = 'speech')

if __name__ == "__main__":
    app.run(debug=True)


