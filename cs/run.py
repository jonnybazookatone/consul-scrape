# encoding: utf-8
"""
Base script file for running routines
"""

import logging
import logging.config
import cs.config as config
from cs.consul_scrape import ConsulScrape

logging.config.dictConfig(config.CS_LOGGING)
logger = logging.getLogger('consul-scrape')


def run(service):
    """
    Pulls config and dumps to s3
    :param service: services to extract and dump to s3
    """

    cs = ConsulScrape(service=service)
    logger.info(
        'Pulling config for services {service} with environment "{environment}" from consul'.format(
            service=service,
            environment=cs.environment
        )
    )
    cs.get_config()

    logger.info(
        'Pushing config from services {service} with environment "{environment}" to s3 bucket {bucket}'.format(
            service=service,
            environment=cs.environment,
            bucket=cs.s3_bucket
        )
    )
    cs.config_to_s3()

if __name__ == '__main__':

    service_list = ['biblib-service']

    run(service=service_list)
