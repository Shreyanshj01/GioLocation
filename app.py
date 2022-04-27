import xml.etree.ElementTree as ET
import json
from flask import Flask, request, Response, jsonify, abort
from flask_cors import CORS, cross_origin
from requests import Session, HTTPError
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from schema_validation import SchemaValidator
from logger_class import get_log

logger = get_log('app')
config_data = json.load(open('config.json'))


retry_strategy = Retry(total=5, status_forcelist=[500, 503, 504], backoff_factor=2)
adapter = HTTPAdapter(max_retries=retry_strategy)
session_object = Session()
session_object.mount("https://", adapter)
session_object.mount("http://", adapter)

app = Flask(__name__)
CORS(app)


def get_response_in_json(response: Response, address: str) -> Response:
    """Construct response in json format

    Args:
        response: Response object received from google map api in json format.
        address: Address for which geolocation data is fetched.

    Return:
        Response: Response object in json format.
    """
    json_response = response.json()
    print(json_response)
    output = {"address": address,
              "coordinates": {"lat": "", "lng": ""}}
    if json_response["status"] == "OK":
        try:
            output["coordinates"] = json_response["results"][0]["geometry"][
                "location"]  # Since geocoding is done for single address
        except KeyError as err:
            logger.error(err)
    else:
        logger.error(f'For given address: "{address}" geolocation not found')
        return Response(f'For given address: "{address}" geolocation not found')
    logger.info("Response generated in json format")
    return jsonify(output)


def get_response_in_xml(response: Response, address: str) -> Response:
    """Construct response in xml format

    Args:
        response: Response object received from google map api in xml format.
        address: Address for which geolocation data is fetched.

    Return:
        Response: Response object in json format.
    """
    xml_response = ET.fromstring(response.text)
    output = ET.Element("root")
    ET.SubElement(output, "address").text = address
    coordinates_element = ET.SubElement(output, "coordinates")
    lat_element = ET.SubElement(coordinates_element, "lat")
    lng_element = ET.SubElement(coordinates_element, "lng")
    lat_element.text = ""
    lng_element.text = ""
    if xml_response.find("status").text == "OK":
        try:
            lat_element.text = xml_response.find("result").find(
                "geometry").find("location").find("lat").text
            lng_element.text = xml_response.find("result").find(
                "geometry").find("location").find("lng").text
        except AttributeError as err:
            logger.error(err)
    else:
        logger.error(f'For given address: "{address}" geolocation not found')
        return Response(f'For given address: "{address}" geolocation not found')
    logger.info("Response generated in xml format")
    return Response(ET.tostring(output, encoding="UTF-8"), mimetype="application/xml")


def get_google_map_data(address: str, output_format: str) -> Response:
    """Get data from google map api.

    Args:
        address: Address for which geolocation data is to be fetch.
        output_format: Format in which response should returned. Allowed format are "json" ans "xml".

    Return:
        response: Response object received from google map api.
    """
    url = config_data["GOOGLE_GEOCODE_API_URL"] + output_format
    parameters = {"address": address, "key": config_data["API_KEY"]}
    response = session_object.get(url=url, params=parameters)
    logger.info("Google Geocode Api URL got called")
    try:
        response.raise_for_status()
    except HTTPError:
        logger.error(f"Received error {response.status_code}:{response.text}")
        abort(500, "Interal Server Error")
    else:
        logger.info(f"google map api response received")
        return response


def get_giolocation(address: str, output_format: str, ) -> Response:
    """Get latitude and longitude for the address given by user.

    Args:
        address: Address for which gioLocation data is to be fetched.
        output_format: Format in which response should returned. Allowed format are "json" ans "xml".

    Return:
        response: A Response object in output format mention in request.
    """
    try:
        google_map_response = get_google_map_data(address=address, output_format=output_format)
        if output_format == 'json':
            response = get_response_in_json(response=google_map_response, address=address)
        else:
            response = get_response_in_xml(response=google_map_response, address=address)
    except Exception as e:
        logger.error(str(e))
    return response


@app.route("/getAddressDetails", methods=['POST'])
@cross_origin()
def get_address_details():
    try:
        logger.info("getAddressDeatails API is called")
        data = request.json

        # Validating payload schema
        _instance = SchemaValidator(response=data)
        error_message = _instance.isTure()
        if len(error_message) > 0:  # Length of response will be greater than 0 in case of invalid payload schema
            logger.error("payload is not in correct schema")
            logger.error("error message send to the user")
            result = jsonify({"status": "error", "message": error_message})
        else:
            # processing to get geolocation data
            logger.info("payload is in correct schema")
            logger.info("calling get_giolocation")
            result = get_giolocation(address=data["address"], output_format=data["output_format"])

    except Exception as e:
        return Response(str(e))

    return result


if __name__ == "__main__":
    app.run(debug=True)  # running the app on the local machine on port 5000
