import requests


def bunkr(token, album_name, files_to_upload):
    album_id = create_album(token, album_name)
    server = get_server(token)
    files = []
    
    for file in files_to_upload:
        #files.append(("files[]", open(file, 'rb')))
        files = (('files[]', open(file, 'rb')),)
        
        '''json_data = {
            'files[]': [open(file, 'rb') for file in files_to_upload]
            }'''
        
        r = requests.post(
            server,
            files=files,
            headers={
                'albumid': str(album_id),
                'token': token
            }
        )
    print(r.json())
    
    return new_album_link(token, album_name, album_id)
    

def new_album_link(token, album_name, album_id):
    json_data = {
        'id': str(album_id),
        'name': album_name,
        'description': '',
        'download': True,
        'public': True,
        'requestLink': True,
    }
    
    r = requests.post(
        'https://app.bunkr.su/api/albums/edit',
        headers={'token': token},
        json=json_data
    )
    
    return "https://bunkr.su/a/" + r.json()['identifier']


def create_album(token, album_name):
    json_data = {
            'name': album_name,
            'description': '',
            'download': True,
            'public': True,
        }
        
    r = requests.post(
        'https://app.bunkr.su/api/albums',
        headers={'token': token},
        json=json_data
    )
    
    return r.json()['id']


def get_server(token):
    r = requests.get('https://app.bunkr.su/api/node', headers={'token': token})
    return r.json()['url']