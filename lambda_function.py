import json
import logging

logger = logging.getLogger('logger')
logger.addHandler(logging.StreamHandler)


def lambda_handler(event, context):
    if 'params' in event:
        if 'log_level' in event['params']:
            logger.setLevel(event['params']['log_level'])

    logger.debug("Received event: " + json.dumps(event, indent=2))
