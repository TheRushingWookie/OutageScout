import grequests
from grequests import map as gmap
from gevent.pool import Pool
from utilities import *
import psycopg2
import json
import logging
import time
import subprocess


try:
    dbconn = psycopg2.connect("dbname='outagescout' host='localhost'")
except:
    print "I am unable to connect to the database"
dbcursor = dbconn.cursor()

def create_db_tables():
    pass

def switch_to_next_proxy():

    pass

def check_services_availability(services):
    """
    Checks if all the services are up and error free. Returns a dict of erroring services.
    
    Args:
        :param dict services: A hash of the services to check for availability. Must contain a 'url' key value pair.
            Example: {"url" : "http://google.com"}, {"url" : "http://adadawdanwdawudad.com"}
    
    Returns:
        dict service_errors: A hash of the services that are erroring and their exceptions. The keys are in JSON form.
            Example {'{"url": "http://adadawdanwdawudad.com"}': ConnectionError(ProtocolError('Connection aborted.', 
                gaierror(8, 'nodename nor servname provided, or not known')),)}
    
    """
    url_to_service_hash = {service['url'] : json.dumps(service) for service in services}
    service_errors = {}
    def handle_error(request, exception):
        print request
        bad_service = url_to_service_hash[request.url]
        service_errors[bad_service] = exception
        import pdb; pdb.set_trace()  # breakpoint b3bfaaba //
    urls = [grequests.get(service['url']) for service in services]
    responses = grequests.map(urls,exception_handler=handle_error, size = 30)

    return service_errors


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,                    format='%(asctime)s - %(message)s',                   datefmt='%Y-%m-%d %H:%M:%S')
    try:
        
        loop_end_time = -1
        while True:
            loop_start_time = time.time()
            check_services_availability([{"url" : "http://google.com"}])   
            loop_end_time = time.time()
            delta_time = loop_end_time - loop_start_time
            sleep_time = 10 - delta_time
            actual_sleep_time = max(0, sleep_time)
            time.sleep(actual_sleep_time)
    except KeyboardInterrupt:
        pass