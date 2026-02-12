from prometheus_client import Counter

REQUEST_COUNTER = Counter('flask_request_count', 'Total number of requests to Flask app')
