#Author : tmr (Abdessamad TEMMAR)
import requests
import string

def get_query_result(base_url,payload,success_text):
        pagecontent = requests.get(base_url, params=payload)
        if pagecontent.text.find(success_text) == 0:
                return True
        else:
                return False

BASE_URL = "http://localhost/index.php"
SUCCESS_TEXT = "Attack Detected !"

guess = False

for str in range(0,255):
	#print "[+] Injecting : "+chr(str)
	PAYLOAD = {'id': chr(str)}
	guess = get_query_result(BASE_URL,PAYLOAD,SUCCESS_TEXT)
	if guess:
		print "[+] "+chr(str)+" is filtred"
