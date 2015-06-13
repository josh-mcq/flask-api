from random import randint, choice
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
match_fields = {
	'home_score': fields.Integer,
    'away_score': fields.Integer,
    
}

class MatchOutcomeAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('home_score', type = int, required = True,
            help = 'No Home Score Provided', location = 'json')
        self.reqparse.add_argument('away_score', type = int, required = True,
            help = 'No Home Score Provided', location = 'json')
        super(MatchOutcomeAPI, self).__init__()

    def get_outcome(self):
        #this has to magically calculate a random score. it mustn't be the exact same for a given game, as it would only be asked one time anyway?
        scoring_range = range(65, 70)
        home_score = choice(scoring_range)
        away_score = choice(scoring_range) 
        while home_score == away_score:
            away_score = choice(scoring_range)   
        return {'home_score':home_score,'away_score':away_score}

    def get(self, matchid):
        match = self.get_outcome()
        return {'outcome': marshal(match, match_fields)}
   
class MatchListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('topic', type=str, location='json')
        self.reqparse.add_argument('event', type=str, location='json')
        self.reqparse.add_argument('data', type=str, location='json')
        super(MatchListAPI, self).__init__()
'''
# for each day, it should generate two matches.  and only if two matches have not been generated for that day already.  or simply use the date as a relatively random way and write a test that verifies that all teams will end up getting an equal number of games over a large number(a season)
    def get(self):
        speech = [speech for speech in speeches if speech['id'] == id]
        if len(speech) == 0:
            abort(404)
        speech = speech[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                speech[k] = v
            return {'speech': marshal(speech, speech_fields)}
'''
#api.add_resource(UserAPI, '/users/<int:id>', endpoint= 'user')
api.add_resource(MatchOutcomeAPI, '/josh/api/v1.0/scores/<string:matchid>', endpoint = 'match')
api.add_resource(MatchListAPI, '/josh/api/v1.0/matches', endpoint = 'matches')

if __name__ == "__main__":
    app.run(debug=True)


