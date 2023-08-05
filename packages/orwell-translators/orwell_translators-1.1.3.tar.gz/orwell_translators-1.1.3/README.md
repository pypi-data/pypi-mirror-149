# Orwell Package For Building Translators

## About

Orwell is an open-source platform that allows you to integrate different metrics collectors into one large super-system, storing the data from different sources in Prometheus' format.
  
With that goal in mind, this package tries to facilitate as much as possible the task of creating translator services compatible with Orwell's architecture.

## Development

If a given service's output follows the scheme "```host```,```metric```,```value```", its translator could be built with the following example:

```
from orwell import Metric, Runner


# The translator function should be able to receive multiple lines
# of the desired service output and return a list of Metric objects

def translate (lines: str) -> list[Metric]:
  metrics = [ line.split(',') for line in lines.split('\n') ]
  return [ Metric(metric, value, { 'host': host }) for host, metric, value in metrics ]


translator = Runner(translate)
translator.run()

```

## Usage

With the example given above we now have three options for running the service:

### Command-Line Mode
```python main.py cmd <output>```

The output will be processed and printed.


### Server Mode
```python main.py server```

A Flask server will start accepting POST requests for /metrics. 
The body of the request must be a dictionary with the only key ```metrics```.
The response will be the processed output whenever the status code is 200.

**Environment Variables**

```FLASK_HOST```
**Default** "localhost"

```FLASK_PORT```
**Default** "5000""

```FLASK_DEBUG```
If set the server will start in debug mode.

### Production Mode
```python main.py prod```

This is the most important mode as it allows to read messages from Kafka and write them to a Redis database, according to the Orwell's architecture.
  
  
**Environment Variables**

```REDIS_HOST```
**Default** "localhost"

```REDIS_PASSWORD```
**Default** "root"

```KAFKA_HOST```
**Default** "localhost""

```KAFKA_PORT```
**Default** 9093

```KAFKA_TOPIC```
**Default** "general"

### Pull Mode
```python main.py pull```

This mode allows gathering data from a custom endpoint.
  
  
**Environment Variables**

```PULL_ENDPOINT```

```PULL_INTERVAL```
**Default** "localhost"

```REDIS_PASSWORD```
**Default** "root"
