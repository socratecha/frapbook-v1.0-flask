from flask import Flask
from flask_restplus import Resource, Api
from flask_restplus import fields

app = Flask(__name__)
api = Api(app)

numbers = [
    { 'id':1, 'number':28, 'description':'2nd perfect number' },
    { 'id':2, 'number':51, 'description':"Looks prime but isn't" },
    { 'id':3, 'number':28, 'description':'7th triangle number' },
]
top_number = 3

number_model = api.model('Favorite Number', {
    'number': fields.Integer(description='The favorite number'),    
    'description': fields.String(description='Description of why it is a favorite')
})

@api.route('/my-api')
class Numbers(Resource):
    def get(self):
        '''Get the full list of favorite numbers'''
        return numbers
    
    @api.expect(number_model)
    def post(self):
        '''Post a new favorite number; server assigns the id'''
        global top_number
        top_number += 1
        numbers.append( {'id':top_number,
                         'number':api.payload['number'],
                         'description':api.payload['description']} )
        return top_number
    
@api.route('/my-api/<int:id>')
class OneNumber(Resource):
    def get(self, id):
        '''Get a single favorite number selected by its id'''
        matches = [ number for number in numbers if number['id'] == id ]
        return matches[0]
