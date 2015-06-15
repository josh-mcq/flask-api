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


]
outcome_fields = {
	'home_period_scores': fields.List(fields.Integer),
    'away_period_scores': fields.List(fields.Integer),
    
}

class MatchOutcomeAPI(Resource):
    #decorators = [auth.login_required]

    def __init__(self):
        ''' Not actually in use right now. '''
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('home_score', type = int, required = True,
            help = 'No Home Score Provided', location = 'json')
        self.reqparse.add_argument('away_score', type = int, required = True,
            help = 'No Home Score Provided', location = 'json')
        super(MatchOutcomeAPI, self).__init__()
   
    def get(self, matchid):
        ''' Return a set of scores, nested in json correctly so that existing PHP code can simply change the URL of the API call.'''
        outcome = self.get_outcome()
        return marshal(outcome, outcome_fields)
        
    
    def get_outcome(self):
        ''' Calculate list of random scores for each quarter. '''
        scoring_range = range(18, 32)
        home_scores = [choice(scoring_range) for q in range(4)]
        away_scores = [choice(scoring_range) for q in range(4)]
        while home_scores == away_scores:
            away_scores = [choice(scoring_range) for q in range(4)]  
        return {'home_period_scores':home_scores,'away_period_scores':away_scores}

event_fields = {}
event_fields['event_id'] = fields.String
event_fields['start_date_time'] = fields.String
event_fields['away_team'] = {}
event_fields['away_team']['team_id'] = fields.String
event_fields['home_team'] = {}
event_fields['home_team']['team_id'] = fields.String
match_fields = {}
match_fields['events_date'] = fields.String
match_fields['event'] = fields.List(fields.Nested(event_fields))




class MatchListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('topic', type=str, location='json')
        self.reqparse.add_argument('event', type=str, location='json')
        self.reqparse.add_argument('data', type=str, location='json')
        super(MatchListAPI, self).__init__()

    def get(self):
        matches = self.get_matches()
        return marshal(matches, match_fields)

    def get_matches(self):
        away_team = {'team_id':"cleveland-cavaliers"}
        home_team = {'team_id':"golden-state-warriors"}
        events_date = "2015-06-14T00:00:00-04:00"
        start_date_time = "hello"
        event_id = "hello"
        event_fields = {"event_id":event_id, "away_team":away_team,
            "start_date_time":start_date_time,"home_team":home_team}
        return {'events_date':events_date, 'event':{"start_date_time":start_date_time, "event_id":event_id, "home_team":home_team, "away_team":away_team}}


api.add_resource(MatchOutcomeAPI, '/josh/api/v1.0/scores/<string:matchid>', endpoint = 'match')
api.add_resource(MatchListAPI, '/josh/api/v1.0/matches', endpoint = 'matches')

if __name__ == "__main__":
    app.run(debug=True)


