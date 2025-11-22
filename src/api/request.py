import requests

url = "http://127.0.0.1:8000/extractor"
files = {'file': open('/home/mehfooj/Desktop/Medical-ocr/medical-data-extraction/src/uploads/pd_1 (1).pdf', 'rb')}
data = {'file_format': 'patient_details'}

response = requests.post(url, files=files, data=data)
result = response.json()

if result['success']:
    print("Extracted Data:", result['data'])
else:
    print("Error:", result['error'])