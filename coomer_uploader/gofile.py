import requests


def gofile(files_to_upload):
    if len(files_to_upload) < 2:
        json_data = single_upload(files_to_upload[0])
        return json_data['data']['downloadPage']
    else:
        url = multiple_upload(files_to_upload)
        return url


def multiple_upload(files_to_upload):
    json_data = single_upload(files_to_upload[0])
    
    options = {
            'token': json_data['data']['guestToken'],
            'folderId': json_data['data']['parentFolder']
        }
    
    for file in files_to_upload[1:]:
        single_upload(file, options)
    
    return json_data['data']['downloadPage']


def single_upload(file, data=None):
    server = get_server()
    files = {'file': open(file, 'rb')}
    r = requests.post(
        f'https://{server}.gofile.io/uploadFile',
        files=files,
        data=data
    )
    
    return r.json()


def get_server():
    r = requests.get('https://api.gofile.io/getServer')
    return r.json()['data']['server']