#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import requests
import os
from requests_toolbelt import MultipartEncoder

requests.packages.urllib3.disable_warnings()

#fill AcunetixUrl field with your Acunetix URL like https://win-6iuauirmri5:3443 
AcunetixUrl = "Acunetix URL"

#fill AcunetixApikey field with your Acunetix Apikey
AcunetixApikey="your Acunetix Apikey ............"

headers = {"X-Auth":AcunetixApikey,"content-type": "application/json"}

def Generate_last_scan_session_id():
	response1 = requests.get(AcunetixUrl+"/api/v1/targets?l=1",headers=headers,timeout=30,verify=False)
	scan_session_id = response1.json()['targets'][0]["last_scan_session_id"]	
	print("last_scan_session_id : " +scan_session_id)
	generate_report_id(scan_session_id)
	
	
def generate_report_id(scan_session_id):
	data = {"export_id":"21111111-1111-1111-1111-111111111111","source":{"list_type":"scan_result","id_list":[scan_session_id]}}
	response2 = requests.post(AcunetixUrl+"/api/v1/exports",data=json.dumps(data),headers=headers,timeout=30,verify=False)
	report_id = response2.json()['report_id']
	print("report_id : " +report_id)
	generate_download_url(report_id)
	
	
def generate_download_url(report_id):
		response3 = requests.get(url=AcunetixUrl + "/api/v1/exports/"+report_id, timeout=10, verify=False, headers=headers)
		response3 = requests.get(url=AcunetixUrl + "/api/v1/exports/"+report_id, timeout=10, verify=False, headers=headers)
		download_url = response3.json()['download'][0]
		print("download_url created: " + AcunetixUrl + download_url)
		export_report(download_url)

		
def export_report(download_url):	
	response4 = requests.get(url=AcunetixUrl + download_url, timeout=10, verify=False, headers=headers)
	with open("acunetix-scan-resault.xml", "wb") as f:
		f.write(response4.content)
	print("Acunetix xml-report-file exported")
	

def Import_Acunetix_Report_Dojo():	
	multipart_data = MultipartEncoder(
		fields={
			#fill this parameter with os address that script exist on it
			'file': ('address of running this script/acunetix-scan-resault.xml', open('acunetix-scan-resault.xml', 'rb'), 'text/plain'),
			#fill other parameters with your correct defetdojo data like ...
            'verified':'true',
			"active":"true",
			'lead':'/api/v1/users/1/',
			'tags':'test1',
			'scan_date':'2019-04-30',
			'scan_type':'Acunetix Scan',
			'minimum_severity':'Info',
			'engagement':'/api/v1/engagements/1/',
			'product':'/api/v1/product/1',
           }
    )
	#fill ApiKey field with your DefectDojo ApiKey like this .. 	
	header = {'content-type': multipart_data.content_type,'Authorization': 'ApiKey admin:469880a9b1b17610491804f373..............'}
	#fill this parameter with your DefectDojo url address like http://192.168.99.100:8080/api/v1/importscan/
	response = requests.post('DefectDojo url address/api/v1/importscan/',data=multipart_data,headers=header)
	print ("Acunetix report imported on DefectDojo")


Generate_last_scan_session_id()
Import_Acunetix_Report_Dojo()