# Install deps with: pip install requests
import os
import requests

from ..sql.log import log_application
from ..common.env import SMS_GATEWAYAPI_TOKEN

def send_sms(recipient: int, msg_content: str, sender: str='AE KF'):
	if len(sender) > 11:
		error_message = 'Sender string too long: ' + sender
		log_application('ERROR', error_message, 'meimbalance.sms')
		raise Exception(error_message)

	token = ""
	try:
		token=os.environ[SMS_GATEWAYAPI_TOKEN]
	except Exception as e:
		log_application('ERROR', str(e), 'meimbalance.sms')
		raise

	payload = {
		"sender": sender,
		"message": msg_content,
		"recipients": [
			{"msisdn": recipient}
		],
	}
	response = ""
	try:
		resp = requests.post(
			"https://gatewayapi.com/rest/mtsms",
			json=payload,
			auth=(token, ""),
		)
		resp.raise_for_status()
		response=resp.json()
		log_application('INFO', str(payload), 'meimbalance.sms')
		log_application('INFO', str(response), 'meimbalance.sms')

	except requests.exceptions.HTTPError as e:
		log_application('ERROR', str(e), 'meimbalance.sms')
		raise
	
	return response
