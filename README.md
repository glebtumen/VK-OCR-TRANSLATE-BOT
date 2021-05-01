# VK-OCR-TRANSLATE-BOT
A free api vk chat bot that takes and translates text from images sent to it by users.
Узнал о такой штуке, как OCR и стало интересно, способен ли я, полный новичок в питоне, написать что-нибудь сносное.
Появилась идея сделать бота, который бы помогал людям в комментариях, которые просят перевод мема.
<br/>
Вот, например, мем:

![alt tag](https://sun9-37.userapi.com/impg/OIPPz2qtdLM2KjxyGi4MYv-PbdBEiqKFAzgV-A/3DEurNpuIRM.jpg?size=389x386&quality=96&sign=b51d71bc66a1c9a0ab7e48f2dd2cb272&type=album "Лайк, если это ты")​
<br/>
<br/>
Человек отправляет мем боту, тот считывает текст с помощью великого OCR и переводит с помощью библиотеки "googletrans==3.1.0a0" - очень важно установить именно эту версию.
<br/>
<br/>
Получается вот такой ответ:
<br/>

![alt tag](https://sun9-58.userapi.com/impg/y7IgfQ16ybqquZVBH1WgGfgMRiaNfzYzl86WQQ/XfBuQ6Nv_QA.jpg?size=401x614&quality=96&sign=6d8ad5e61b697b6608d7468b009405f4&type=album "Лайк, если это ты")

<br/>

 Возможно в дальнейшем буду улучшать, в частности нужно найти новую более приемлемую OCR, потому что эта считывает только по строчке и не переводит целыми абзацами. Всем спасибо за внимание!
