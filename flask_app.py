'''
.. epigraph::

    *It’s like asking why is Ludwig van Beethoven’s Ninth Symphony 
    beautiful. If you don't see why, someone can't tell you. I know 
    numbers are beautiful. If they aren't beautiful, nothing is.*
    -- Paul Erdos

The Numbers API is for when you *really* must track your **favorite**
**numbers**.

.. warning::
   This implementation does not persist data across sessions. Also, if
   it is run with multiple server processes, their data will not
   synchronize.
'''
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
        '''Get the full list of favorite numbers

        :route: ``/my-api`` GET
        :return: 
           A list of favorite numbers, each with:
              * ``id`` a unqiue int identifier
              * ``number`` the favorite number
              * ``description`` the reason it is a favorite
        '''
        return numbers
    
    @api.expect(number_model)
    def post(self):        
        '''Post a new favorite number; server assigns the id

        Appends a favorite number with a description into the
        collection, assigning it a new unique identifier in the
        collection. Returns the new identifier.

        :route: ``/my-api`` POST
        :payload:
           Submit a JSON object with:
              * ``number``: the new favorite number (int)
              * ``description``: reason it's a favorite (str)

        :error: **400** if missing either ``number`` or ``description`` field
        :return: Newly assigned identifier
        '''
        if not ('number' in api.payload and 'description' in api.payload):
            api.abort(400, "Payload must include number and description")
        global top_number
        top_number += 1
        numbers.append( {'id':top_number,
                         'number':api.payload['number'],
                         'description':api.payload['description']} )
        return top_number
    
@api.route('/my-api/<int:id>')
class OneNumber(Resource):
    def get(self, id):
        '''Get a single favorite number selected by its id
        
        Gets both the number and the description of why its a
        favorite number if the id is valid, otherwise produces an
        error code. 

        :route: ``/my-api/<int:id>`` GET
        :param id: favorite number identifier
        :type id: int

        :error: **404** if ``id`` is not in the collection
        :return: 
           A single favorite number with:
              * ``id`` a unqiue int identifier
              * ``number`` the favorite number
              * ``description`` the reason it is a favorite
        '''
        matches = [ number for number in numbers if number['id'] == id ]
        if len(matches) == 0:
            api.abort(404, "Unique id {} not found".format(id))
        return matches[0]
