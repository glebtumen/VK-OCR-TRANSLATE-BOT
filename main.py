# requirements
# googletrans==3.1.0a0
# vk_api
# requests
# google-cloud-vision

import vk_api
import requests
import json
import os
from googletrans import Translator
from vk_api.longpoll import VkLongPoll, VkEventType
from google.cloud import vision
from google.cloud.vision_v1 import AnnotateImageResponse

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'get it from Google cloud'
client = vision.ImageAnnotatorClient()


vk_session = vk_api.VkApi(token='get it from VK group')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

translator = Translator()


#idk like it is just a function
def f():
    pass

def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(
        image=image,
        image_context={"language_hints": ["bn"]},)

    serialized_proto_plus = AnnotateImageResponse.serialize(response)
    response = AnnotateImageResponse.deserialize(serialized_proto_plus)
    # print(response.full_text_annotation.text)

    # serialize / deserialize json
    response_json = AnnotateImageResponse.to_json(response)
    response = json.loads(response_json)
    l_response = response['fullTextAnnotation']['text']
    l_response = l_response.replace('\n',' ')
    return l_response



for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:  #translates only text messages
        mesag = event.text.capitalize()
        result = translator.translate(mesag, src='en', dest='ru')
        vk.messages.send(peer_id=event.peer_id, random_id=0, message=result.text)

    if event.type == VkEventType.MESSAGE_NEW and event.to_me: #translates text from photos
        message_id = event.message_id
        msg = vk.messages.getById(message_ids=message_id)
        # print(msg)
        type = msg['items'][0]['attachments'] #get type of attachments
        # print(type)
        if not type:
            vk.messages.send(peer_id=event.peer_id, random_id=0, message='Пожалуйста, отправьте изображение')
        else:
            type_type = msg['items'][0]['attachments'][0]['type']
            if type_type != 'photo':
                vk.messages.send(peer_id=event.peer_id, random_id=0, message='Пожалуйста, отправьте изображение')
            else:
                owner_id = event.peer_id
                access_key = msg['items'][0]['attachments'][0]['photo']['access_key']
                url_photo = msg['items'][0]['attachments'][0]['photo']['sizes'][4]['url']

                super_response = detect_text_uri(url_photo)

                if super_response == '':
                    vk.messages.send(peer_id=event.peer_id, random_id=0,
                                     message='Невозможно перевести. Плохое качество изображения.')
                else:
                    result_translated = translator.translate(super_response, src='en', dest='ru')
                    vk.messages.send(peer_id=event.peer_id, random_id=0, message=result_translated.text)

