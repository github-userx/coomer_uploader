import requests


def pixeldrain(files_to_upload):
    ids = []
    
    for file in files_to_upload:
        files = {'file': open(file, 'rb')}
        
        r = requests.post(
            'https://pixeldrain.com/api/file/',
            files=files
        )
        
        ids.append(r.json()['id'])
    
    identifier = create_list(ids)
    return f"https://pixeldrain.com/l/{identifier}"


def create_list(ids):        
    json_data = {
        'anonymous': True, 
        'files': [{'id': idd} for idd in ids]
        }
    
    r = requests.post('https://pixeldrain.com/api/list', json=json_data)
    return r.json()['id']