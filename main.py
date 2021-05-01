import vk_api
from googletrans import Translator
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import json

vk_session = vk_api.VkApi(token='TAKE_THIS_TOKEN_FROM_YOUR_GROUP_VK')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

translator = Translator()

#idk like it is just a function
def f(): 
    pass

#Main ocr thing that reads text from images. It is free so quality of reading is not impressive
#To get api you need to register on their cite
def ocr_space_url(url, overlay=False, api_key='PUT_YOUR_KEY_HERE', language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'apikey': api_key,
               'url': url,
               'language': language,
               'scale': True,
               'isTable': True,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()

#Cycle for listening events such as messages and photos
for event in longpoll.listen():
    
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:  #translates only text messages
        mesag = event.text.capitalize()
        result = translator.translate(mesag, src='en', dest='ru')
        vk.messages.send(peer_id=event.peer_id, random_id=0, message=result.text)

    if event.type == VkEventType.MESSAGE_NEW and event.to_me: #translates text from photos
        message_id = event.message_id
        msg = vk.messages.getById(message_ids=message_id)
        type = msg['items'][0]['attachments'] #get type of attachments
        if not type:
            f()
        else:
            owner_id = event.peer_id
            access_key = msg['items'][0]['attachments'][0]['photo']['access_key']
            url = msg['items'][0]['attachments'][0]['photo']['sizes'][4]['url']
            photo_id = msg['items'][0]['attachments'][0]['photo']['id']
            photo = f'photo{owner_id}_{photo_id}_{access_key}' 

            # vk.messages.send(peer_id=event.peer_id, random_id=0, attachment=photo) #пересылает пост обратно пользователю

            test_url = ocr_space_url(url=url)
            test_url = json.loads(test_url)
            text_detected = test_url.get('ParsedResults')[0].get('ParsedText')
            #print(text_detected)
            result_translated = translator.translate(text_detected, src='en', dest='ru')
            vk.messages.send(peer_id=event.peer_id, random_id=0, message=result_translated.text)

