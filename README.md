# Fetch Rewards Coding Assessment
- **Candidate:** Christian Normand
- **Position:** Machine Learning Apprenticeship
- **Date:** March 23, 2022

## How to run this code
My submission is packaged as a containerized REST API, and you can pull an image from Docker Hub with the following command:

```bash
$ docker pull ctnormand1/fetch-ml-technical-project
```

Once you've pulled the image into your local environment, run the container with the following command:

```bash
$ docker run -d -p 8000:5000 --rm ctnormand1/fetch-ml-technical-project
```

## Interacting with the API
### Request and response format
The API listens for `POST` requests at the host root. Data must be formatted as JSON and contained in the request body. An example is shown below:

```json
{
  "image_dimensions": [3, 3],
  "corner_points": [[0, 0], [0, 2], [2, 2], [2, 0]]
}
```

If the request is valid, the API will respond with a JSON array of pixel coordinates starting at the top-left corner. For example, the request from above would produce the following response:

```json
{
  "pixels": [
    [[0.0, 2.0], [1.0, 2.0], [2.0, 2.0]],
    [[0.0, 1.0], [1.0, 1.0], [2.0, 1.0]],
    [[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]]
  ]
}
```

### Sending requests with Python
The following code snippet shows how you can use Python to interact with the API. Note: you can pass coordinates as either tuples or lists. The Python requests module will convert them to valid JSON arrays.

```python
import requests

payload = {
    'corner_points': [(0, 0), (0, 2), (2, 2), (2, 0)],
    'image_dimensions': (3, 3)
}
r = requests.post('http://localhost:8000/', json=payload)

print(r.json())
```

### Sending requests with curl
You can also use curl to send a request in your command terminal.

```bash
$ curl  curl -d '{"image_dimensions": [3, 3], "corner_points": [[0, 0], [0, 2],
[2, 2], [2, 0]]}' -H "Content-Type: application/json"
-X POST http://localhost:8000
```

## Additional features
### Request validation
Given enough time, users (including internal ones) will always find a way to break your program. That said, it's the programmer's responsibility to design robust applications that can handle unexpected input. The validation that I built into the API identifies invalid requests that would otherwise break the application.

### Unit tests
Testing is a critical part of app development, especially for more complex apps that are being worked on by multiple developers. Although this app is simple, I included a few unit tests in `tests.py`.

## References
- [Miguel Grinberg's Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
(My go-to anytime I need to build a Flask app :thumbsup:)
