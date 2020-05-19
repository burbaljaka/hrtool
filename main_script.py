import xlrd, json
import os
import requests
#Path input from user
# print('Input a path to the base')
# path = input()
path = "C:\\Users\\tim\\Downloads\\Тестовое задание Python\\Тестовое задание\\Тестовая база.xlsx"
workbook = xlrd.open_workbook(path)

#Getting path to the DB folder
db_folder_list = path.split('\\')[0:-1]
db_folder_path = ''
for i in range(len(db_folder_list)):
    if i == 0:
        db_folder_path += db_folder_list[i]
    else:
        db_folder_path += '\\' + db_folder_list[i]
#opening db file to get applicants
worksheet = workbook.sheet_by_index(0)
print('Обрабатываю базу')

data = []
positions = set()
for row in range(1, worksheet.nrows):

    applicant = {}
    applicant['position'] = worksheet.cell_value(row, 0)
    applicant['name'] = worksheet.cell_value(row, 1)
    applicant['calary'] = worksheet.cell_value(row, 2)
    applicant['comment'] = worksheet.cell_value(row, 3)
    applicant['status'] = worksheet.cell_value(row, 4)
    data.append(applicant)
    positions.add(applicant['position'])

print('Нашел {} кандидатов, {} позиций'.format(len(data), len(positions)))

#Getting list of accounts to work with and taking the first one
url = 'https://dev-100-api.huntflow.ru/'

token = '71e89e8af02206575b3b4ae80bf35b6386fe3085af3d4085cbc7b43505084482'
headers = {'Authorization': 'Bearer '+token}

response = requests.get(url+'accounts', headers=headers)
account_id = json.loads(response.text)['items'][0]['id']
print(account_id)

#Getting a list of account vacancies
print('Получаю список вакансий')
response = requests.get(url+'account/{}/vacancies/'.format(account_id), headers=headers)
vacancies_response = json.loads((response.text).encode('utf-8'))['items']

print(vacancies_response)

#Getting a list of vacancies names
vac_names = []
for vac in vacancies_response:
    vac_names.append(vac['position'])

print(vac_names)
uploading_result = {}
uploading_headers = headers
uploading_headers['X-File-Parse'] = 'true'
uploading_url = url + 'account/{}/upload'.format(account_id)
items = []
#Scanning db folder to get CV of applicants for appropriate position
with os.scandir(db_folder_path) as dir_entries:
    # file_to_upload = os.path.join(db_folder_path, 'Frontend-разработчик', 'Глибин Виталий Николаевич.doc')
    # print(file_to_upload)
    # files = [('file', open(file_to_upload, 'rb'))]

    # file_sent = requests.request('POST', uploading_url, files=files, headers=uploading_headers)
    # file_sent = requests.post('http://httpbin.org/post', files=files, headers=uploading_headers)
    # print(file_sent.text)
    # print(file_sent.json()['headers'])
    for entry in dir_entries:
        print(entry.name)
        if entry.name in vac_names:
            with os.scandir(os.path.join(db_folder_path, entry.name)) as subdir_entries:
                for folder in subdir_entries:
                    items.append(folder)

for elem in items:
    print(elem)
    file_sent = requests.request("POST", uploading_url, files={'file': open(elem.path, 'rb')}, data={}, headers=uploading_headers)
    print(file_sent.text)