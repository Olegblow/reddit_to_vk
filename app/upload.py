import os
import vk_api
from typing import List
from celery import shared_task
import datetime


# vk 
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', '')
GROUP_ID = '-178535034'
MESSAGE = '#meme #game #reddit #bot'


def start_upload() -> None:
    """Запускает загрузку изображений в вк через таски."""
    # 1. Получаю кол-во изображений в папке.
    path = 'img/'
    img_list = get_img_list(path)
    img_count = len(img_list)
    # 2. считаем делей. для каждой картинки
    delta = 18/img_count
    hour = int(delta)
    minute = (int(delta*100%100) * 6)/100
    # 3. Запускаю цикл отправки изображений на стену.
    now = datetime.datetime.now()
    delta = datetime.timedelta(seconds=(hour*3600 + minute*60))
    for img  in img_list:
        upload_task.apply_async(
            eta=now,
            kwargs={'img': img, 'path': path}
        )
        now += delta


def get_img_list(path: str) -> List:
    """Возвращает список файлов с расширением jpg и png."""
    return [f for f in os.listdir(path) if f.endswith('.jpg') or f.endswith('.png')]


@shared_task
def upload_task(img:str, path: str) -> None:
    """Таск загрузки изображений на стену в группы в вк."""
    vk_session = vk_api.VkApi(token=ACCESS_TOKEN)
    upload = vk_api.VkUpload(vk_session)
    img_path=os.path.join(path, img)
    uploaded_img = upload.photo_wall(	
            photos=img_path
    )
    attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in uploaded_img)
    vk_session.method("wall.post", {
        'owner_id': GROUP_ID,
        'message': MESSAGE,
        'attachment': attachment,
    })
    # удалить картинку.
    os.remove(img_path)