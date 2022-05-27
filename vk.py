import requests
import json

token_vk = input('Введите токен vk: ')
token_ya = input('Введите яндекс токен: ')
id_vk = input('Введите id вконтакте: ')   #сделать проверку?
save_json = {}
json_work = {}

class Vk:
    url_ya = 'https://cloud-api.yandex.net'

    def __init__(self, token_vk, token_ya):
        self.token_vk = token_vk
        self.token_ya = token_ya
        
    def get_headers_ya(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token_ya}'
        }

    def put_new_folder(self, path=id_vk):
        url = f'{self.url_ya}/v1/disk/resources/'
        headers = self.get_headers_ya()
        params = {'path': path}
        response = requests.put(url, params=params, headers=headers)
        # print(f'Папка с именем {path} создана!')
        return str(path) + "/"  

    def get_photos(self, count_photo=5):
        params = {
            'owner_id': id_vk,
            'album_id': 'profile',
            'extended': 1,
            'count': count_photo,                 
            'photo_sizes': 1,             #не уверен нужно ли это, работает одинаково и без этого параметра
            'access_token': self.token_vk,
            'v': '5.131'
            }
        url = 'https://api.vk.com/method/photos.get'
        res = requests.get(url, params = params)
        global get_photos_json
        get_photos_json = res.json()
        self.save_file_info()
        self.file_for_load()
        return get_photos_json, self.load()

    def save_file_info(self):  
        for id,item in enumerate(get_photos_json['response']['items']):
            save_json['file_name'] = get_photos_json['response']['items'][id]['likes']['count']
            save_json['size'] = {}
            save_json['size']['height'] = get_photos_json['response']['items'][id]['sizes'][-1]['height']
            save_json['size']['width'] = get_photos_json['response']['items'][id]['sizes'][-1]['width']
            with open('file_info.json', 'a') as text:
                json.dump(save_json, text, indent=2)  

    def file_for_load(self):  
        for id,item in enumerate(get_photos_json['response']['items']):
            json_work[id] = {}
            json_work[id]['file_name'] = get_photos_json['response']['items'][id]['likes']['count']
            json_work[id]['size'] = {}
            json_work[id]['size']['height'] = get_photos_json['response']['items'][id]['sizes'][-1]['height']
            json_work[id]['size']['width'] = get_photos_json['response']['items'][id]['sizes'][-1]['width']
            json_work[id]['url'] = get_photos_json['response']['items'][id]['sizes'][-1]['url']
                   
    def upload(self, path_to_ya, url_vk):
        url = f'{self.url_ya}/v1/disk/resources/upload/'
        headers = self.get_headers_ya()
        params = {'path': self.put_new_folder()+path_to_ya, 'url': url_vk}
        response = requests.post(url, params=params, headers=headers)             
        # print(response)
        
    def load(self):
        count = 0
        for i in json_work:
            self.upload(str(json_work[i]['file_name']), json_work[i]['url'])
            count += 1
            print(f'Загружено {count} фотографий из {len(json_work)}')

vk = Vk(token_vk, token_ya)
vk.get_photos()
