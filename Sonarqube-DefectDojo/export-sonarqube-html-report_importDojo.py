
import requests
import os
from requests_toolbelt import MultipartEncoder

		
def Export_Html_Report():
	#fill sonarurl,sonarcomponent,project and sonartoken fields with your correct data like this ..
	os.system('sonar-report --sonarurl="http://192.168.6.128:9000" --sonarcomponent="webgoat" --project="webgoat" --sonartoken="9e1646a584d3ba7a70......................" --noSecurityHotspot="true" --allbugs="false"  > sonar-report.html')
	print ("SonarQube HTML report exported")


def Import_Sonar_Report_Dojo():	
	multipart_data = MultipartEncoder(
		fields={
			##fill this parameter with os address that script exists on it like ...
            'file': ('C:\sonar-report.html', open('sonar-report.html', 'rb'), 'text/plain'),
			#fill other parameters with your correct defetdojo data like ...
			'verified':'true',
			"active":"true",
			'lead':'/api/v1/users/1/',
			'tags':'test1',
			'scan_date':'2019-04-30',
			'scan_type':'SonarQube Scan',
			'minimum_severity':'Info',
			'engagement':'/api/v1/engagements/1/',
			'product':'/api/v1/product/1',
           }
    )
	#fill ApiKey field with your DefectDojo ApiKey like this ...
	header = {'content-type': multipart_data.content_type,'Authorization': 'ApiKey admin:469880a9b1b17610491804..................'}
	#fill this parameter with your DefectDojo url address like ..
	response = requests.post('http://192.168.99.100:8080/api/v1/importscan/',data=multipart_data,headers=header)
	print ("SonarQube report imported on DefectDojo")
	
	
Export_Html_Report()
Import_Sonar_Report_Dojo()