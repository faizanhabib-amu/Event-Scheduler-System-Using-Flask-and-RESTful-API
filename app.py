# Importing necessary modules and libraries
from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
import datetime
import json

# Initialize Flask app
app = Flask(__name__)
api = Api(app)

# Define the JSON file to store events data
EVENTS_FILE = "events.json"

# Function to load events from the JSON file
def load_events():
    try:
        with open(EVENTS_FILE, "r") as f:
            events_data = json.load(f)
            
            # Convert timestamp strings to datetime objects
            for event in events_data:
                event['start_time'] = datetime.datetime.strptime(event['start_time'], '%Y-%m-%d %H:%M:%S')
                event['end_time'] = datetime.datetime.strptime(event['end_time'], '%Y-%m-%d %H:%M:%S')

            return events_data
    except FileNotFoundError:
        return []  # If file not found, initialize with an empty list


# Function to save events to the JSON file
def save_events(events):
    with open(EVENTS_FILE, "w") as f:
        json.dump(events, f, default=str, indent=4)

# Load events from the JSON file
events = load_events()

# Define fields for event serialization
event_fields = {
    'title': fields.String,
    'description': fields.String,
    'start_time': fields.DateTime(dt_format='iso8601'),
    'end_time': fields.DateTime(dt_format='iso8601')
}

# Resource for listing all events and creating new events
class EventListResource(Resource):
    # GET method to retrieve all events
    @marshal_with(event_fields)
    def get(self):
        sorted_events = sorted(events, key=lambda x: x['start_time'])
        return sorted_events

    # POST method to create a new event
    @marshal_with(event_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title is required')
        parser.add_argument('description', type=str, required=True, help='Description is required')
        parser.add_argument('start_time', type=str, required=True, help='Start time is required (format: YYYY-MM-DD HH:MM:SS)')
        parser.add_argument('end_time', type=str, required=True, help='End time is required (format: YYYY-MM-DD HH:MM:SS)')
        args = parser.parse_args()

        # Create event object
        event = {
            'title': args['title'],
            'description': args['description'],
            'start_time': datetime.datetime.strptime(args['start_time'], '%Y-%m-%d %H:%M:%S'),
            'end_time': datetime.datetime.strptime(args['end_time'], '%Y-%m-%d %H:%M:%S')
        }
        events.append(event)  # Add event to list
        save_events(events)   # Save events to file
        return event, 201     # Return created event with HTTP status code 201

# Resource for updating and deleting a specific event
class EventResource(Resource):
    # PUT method to update an existing event
    @marshal_with(event_fields)
    def put(self, event_id):
        if 0 <= event_id < len(events):  # Check if event ID is valid
            parser = reqparse.RequestParser()
            parser.add_argument('title', type=str)
            parser.add_argument('description', type=str)
            parser.add_argument('start_time', type=str)
            parser.add_argument('end_time', type=str)
            args = parser.parse_args()

            event = events[event_id]  # Get the event object
            # Update event properties if provided in request
            if 'title' in args:
                event['title'] = args['title']
            if 'description' in args:
                event['description'] = args['description']
            if 'start_time' in args:
                event['start_time'] = datetime.datetime.strptime(args['start_time'], '%Y-%m-%d %H:%M:%S')
            if 'end_time' in args:
                event['end_time'] = datetime.datetime.strptime(args['end_time'], '%Y-%m-%d %H:%M:%S')

            save_events(events)  # Save updated events to file
            return event         # Return updated event
        else:
            return {'error': 'Event not found'}, 404  # Return error if event ID not found

    # DELETE method to delete an existing event
    def delete(self, event_id):
        if 0 <= event_id < len(events):  # Check if event ID is valid
            del events[event_id]         # Delete event from list
            save_events(events)          # Save updated events to file
            return {'message': 'Event deleted successfully'}  # Return success message
        else:
            return {'error': 'Event not found'}, 404  # Return error if event ID not found

# Add resources to the API
api.add_resource(EventListResource, '/events')
api.add_resource(EventResource, '/events/<int:event_id>')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
