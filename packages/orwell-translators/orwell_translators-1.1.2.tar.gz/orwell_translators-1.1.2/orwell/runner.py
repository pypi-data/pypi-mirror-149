from sys import argv, stderr
from os import environ

from .helper import Helper
from .translator import Translator


class Runner: 
  CMD_TEXT = 'cmd'
  SERVER_TEXT = 'server'
  PROD_TEXT = 'prod'
  PULL_TEXT = 'pull'

  def __init__(self, translation_function: callable) -> None:
      self._translator = Translator(translation_function)

  def run (self):
    RUN_MODES = [ Runner.CMD_TEXT, Runner.SERVER_TEXT, Runner.PROD_TEXT, Runner.PULL_TEXT ]

    if len(argv) < 2 or argv[1] not in RUN_MODES:
      print("Run mode not recognised!\nUsage: python " + __file__ + " <run_mode> [OPTIONS]\nAvailable modes: " + ", ".join(RUN_MODES), file=stderr)

    elif argv[1] == Runner.CMD_TEXT:
      print(Helper.concatenate_metrics([self._translator.translate(a) for a in argv[2].split('\\n')]))

    elif argv[1] == Runner.SERVER_TEXT:
      args = {}

      flask_host = environ.get('FLASK_HOST')
      flask_port = environ.get('FLASK_PORT')
      flask_debug = environ.get('FLASK_DEBUG')

      if flask_host is not None: args['host'] = flask_host
      if flask_port is not None: args['port'] = flask_port
      if flask_debug is not None: args['debug'] = True

      self._translator.serve(**args)

    elif argv[1] == Runner.PROD_TEXT:
      args = {}

      redis_password = environ.get('REDIS_PASSWORD')
      kafka_host = environ.get('KAFKA_HOST')
      kafka_port = environ.get('KAFKA_PORT')
      kafka_topic = environ.get('KAFKA_TOPIC')

      if redis_password is not None: args['redis_password'] = redis_password
      if kafka_host is not None: args['kafka_host'] = kafka_host
      if kafka_port is not None: args['kafka_port'] = kafka_port
      if kafka_topic is not None: args['kafka_topic'] = kafka_topic

      self._translator.prod(**args)

    elif argv[1] == Runner.PULL_TEXT:
      args = {}

      pull_endpoint = environ.get('PULL_ENDPOINT')
      pull_interval = environ.get('PULL_INTERVAL')
      redis_password = environ.get('REDIS_PASSWORD')

      if pull_endpoint is not None: args['endpoint'] = pull_endpoint
      if pull_interval is not None: args['interval'] = int(pull_interval)
      if redis_password is not None: args['redis_password'] = redis_password

      self._translator.pull(**args)