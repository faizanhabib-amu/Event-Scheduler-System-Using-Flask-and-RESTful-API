# Event-Scheduler-System-Using-Flask-and-RESTful-API

This is a simple Python Flask app that acts as a RESTful API for event management. It allows users to interact with event data through HTTP requests. The app enables users to:

1. **Create**: Users can create new events by sending a POST request with event details.
2. **Read**: Users can retrieve a list of all events or specific event details by sending GET requests.
3. **Update**: Existing events can be updated by sending a PUT request with modified event details.
4. **Delete**: Events can be deleted using a DELETE request.

The app utilizes Flask for web development and Flask-RESTful to streamline the creation of RESTful APIs. Event data is stored in a JSON file, and the app handles serialization and deserialization of this data. It provides endpoints for managing events and utilizes datetime for handling date and time information.

This Flask app has been tested using POSTMAN, a popular API testing tool. POSTMAN allows users to send various types of HTTP requests (GET, POST, PUT, DELETE) to the defined endpoints of the Flask app and observe the responses.

By testing the app with POSTMAN, users can verify that the API endpoints behave as expected, ensuring that events can be created, retrieved, updated, and deleted successfully. Testing with POSTMAN helps validate the functionality and reliability of the API before deploying it for production use.
