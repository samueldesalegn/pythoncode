import boto3 
from datetime import datetime, timedelta
from requests_aws4auth import AWS4Auth
import requests
import pprint

pp = pprint.PrettyPrinter(indent=4)

idp = boto3.client('cognito-identity', 'us-east-1')
id_response = idp.get_id(IdentityPoolId='us-east-1:4d066985-77cb-4b8b-848d-1dc7c854715c')
credentials = idp.get_credentials_for_identity(IdentityId=id_response["IdentityId"])

auth=AWS4Auth(
	credentials["Credentials"]["AccessKeyId"],
	credentials["Credentials"]["SecretKey"],
	'us-east-1',
	'geo',
	session_token=credentials["Credentials"]["SessionToken"]
)

body = {
	"text": "600 Cannon Rd, Silver Spring, MD USA"
}

response = requests.post('https://places.geo.us-east-1.amazonaws.com/places/v0/indexes/sampleIndex/search/text', auth=auth, json=body)

best = response.json()["Results"][0]
pp.pprint(best)
