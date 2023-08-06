import lxml.html
import requests as rq

#from azure.storage.blob import BlobClient, BlobServiceClient


def copernicus_marine_login(url, user, pwd):
    """
    Open a connection to Copernicus Marine CAS with user credentials.
    __author__     = "Copernicus Marine User Support Team"
    __copyright__  = "(C) 2021 E.U. Copernicus Marine Service Information"
    __credits__    = ["E.U. Copernicus Marine Service Information"]
    __license__    = "MIT License - You must cite this source"
    __version__    = "202104"
    __maintainer__ = "D. Bazin, E. DiMedio, C. Giordan"
    __email__      = "servicedesk dot cmems at mercator hyphen ocean dot eu"

    Parameters
    ----------
    username : str
        Copernicus Marine Username, provided for free from https://marine.copernicus.eu .
    password : str
        Copernicus Marine Password, provided for free from https://marine.copernicus.eu .

    Returns
    -------
    bool
        Returns ``conn_session`` if credentials are correct, ``False`` otherwise.

    """
    params = {'service': url}
    cmems_cas_url = 'https://cmems-cas.cls.fr/cas/login'
    conn_session = rq.session()
    login_session = conn_session.get(cmems_cas_url, params=params)
    login_from_html = lxml.html.fromstring(login_session.text)
    hidden_elements_from_html = login_from_html.xpath(
        '//form//input[@type="hidden"]')
    payload = {
        he.attrib['name']: he.attrib['value']
        for he in hidden_elements_from_html
        }
    payload['username'] = user
    payload['password'] = pwd
    conn_session.post(cmems_cas_url, data=payload, params=params)

    return conn_session


def submit_request(url, payload, conn_session):

    print("submitting request")
    response = conn_session.get(url, params=payload)
    # do something with the response...
    request_id = None
    return request_id


def check_status(url, request_id, conn_session):
    print("checking status")
    params = {
        "action": "getreqstatus",
        "requestid": int(request_id)
        }
    response = conn_session.get(url, params=params)

    response_xml = lxml.html.fromstring(response.text)
    request_id = response_xml.attrib['remoteuri']
    print(request_id)
    
    print(response.text)
    # print(response.url)
    # print(response.status_code)
    # print(response.text)
    return True, ""#dl_url


def download_data(url, payload, output_filename, conn_session):

    #req = conn_session.get(url, stream=True)
    print(url)
    req = conn_session.get(url, params=payload, stream=True)
    print(req.request.url)
    print(req.request.body)
    print(req.status_code)
    with open(output_filename, 'wb') as of:
        for chunk in req.iter_content(chunk_size=1000000):
            of.write(chunk)
    
    return True


# def download_to_blob(url, payload, output_filename, conn_session):

#     req = conn_session.get(url, params=payload, stream=True)

#     #blob_client = BlobClient.from_blob_url(blob_url=, credential=,)

#     BlobClient.upload_blob_from_url(req.request.url)

#     # with open(output_filename, 'rb') as blob_file:
#     #     for chunk in req.iter_content(chunk_size=1000000):
#     #         blob_client.upload_blob(data=chunk)
    
#     return True


def order_payload(date_min, date_max, lon_min=-180., lon_max=180., lat_min=68., lat_max=90., mode='console'):

    payload = {
        "action": "productdownload",
        "service": "ARCTIC_ANALYSIS_FORECAST_PHYS_002_001_a-TDS",
        "product": "dataset-topaz4-arc-1hr-myoceanv2-be",
        "t_lo": date_min,
        "t_hi": date_max,
        "x_lo": lon_min,
        "x_hi": lon_max,
        "y_lo": lat_min,
        "y_hi": lat_max,
        "variable": ["latitude", "longitude", "uice", "vice"],
        "mode": mode,
    }

    return payload
