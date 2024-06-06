import requests
from pathlib import Path

# Geonetwork username and password:
username = ''
password = ''

# Geonetwork and CKAN server URLs
GN_URL = "http://localhost:8080"
CKAN_URL = "http://localhost:5000"

def get_gn_xsrf_token(session):
    """ Retrieves XSRF token from Geonetwork

    :param session: requests Session object
    :returns: XSRF as string or None upon error
    """
    authenticate_url = GN_URL + '/geonetwork/srv/eng/info?type=me'
    response = session.post(authenticate_url)

    # Extract XRSF token
    xsrf_token = response.cookies.get("XSRF-TOKEN")
    if xsrf_token:
        return xsrf_token
    return None

def list_ckan_records():
    """ Contacts CKAN and retrieves a list of package ids for all public records

    :returns: list of package id strings or None upon error
    """
    session = requests.Session()
    url_path =  Path('api') / '3' / 'action' / 'package_list'
    url = f'{CKAN_URL}/{url_path}'
    r = session.get(url)
    resp = r.json()
    # print("resp=", resp)
    if resp['success'] is False:
        return None
    return resp['result']

def get_ckan_record(package_id):
    """ Given a package id retrieves its record metadata

    :param package_id: CKAN package_id string
    :returns: package metadata as a dict or None upon error
    """
    session = requests.Session()
    # Set up CKAN URL
    url_path =  Path('api') / '3' / 'action' / 'iso19115_package_show'
    url = f'{CKAN_URL}/{url_path}'
    r = session.get(url, params={'format':'xml', 'id':package_id})
    # print("json:", r.json())
    resp = r.json()
    if resp['success'] is False:
        return None
    return resp['result']
    

def insert_gn_record(session, xsrf_token, xml_string):
    """ Inserts a record into Geonetwork

    :param session: requests Session object
    :param xsrf_token: Geonetwork's XSRF token as a string
    :param xml_string: XML to be inserted as a string
    :returns: True or False if insert succeeded
    """
    # Set header for connection
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/xml',
               'X-XSRF-TOKEN': xsrf_token
    }

    # Set the parameters
    # Currently 'uuidProcessing' is set to 'NOTHING' so that records that
    # already exist are rejected by Geonetwork as duplicates
    params = {'metadataType': 'METADATA',
              'file': 'bucketname',
              'updateDateStamp': 'true',
              'recursiveSearch': 'false',
              'publishToAll': 'true',
              'assignToCatalog': 'false',
              'uuidProcessing': 'NOTHING',  # Available values : GENERATEUUID, NOTHING, OVERWRITE
              'rejectIfInvalid': 'false',
              'transformWith': '_none_'
    }

    # Send a put request to the endpoint to create record
    response = session.put(GN_URL + '/geonetwork/srv/api/0.1/records',
                        data=xml_string,
                        params=params,
                        auth=(username, password),
                        headers=headers
    )
    resp = response.json()

    # Check if record was created in Geonetwork
    if response.status_code == requests.codes['created'] and resp['numberOfRecordsProcessed'] == 1 and \
            resp['numberOfRecordsWithErrors'] == 0:
        print("Inserted")
        return True
    print(f"Insert failed: status code: {response.status_code}\n{resp}")
    return False
        

if __name__ == "__main__":
    session = requests.Session()
    xsrf = get_gn_xsrf_token(session)
    if xsrf is not None:
        for id in list_ckan_records():
            print(f"Inserting '{id}'")
            xml_string = get_ckan_record(id)
            if xml_string is not None:
                insert_gn_record(session, xsrf, xml_string)
            else:
                print("Could not get record from CKAN")
    

