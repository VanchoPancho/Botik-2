from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api
import random
import requests
import goslate


vk = vk_api.VkApi(token="8a09d5002083750539abc1de2c1cb8f4516d0706179c0b3a0fdb73215554ce39bc99ba3edbcbdf31e9300")

vk._auth_token()

vk.get_api()

longpoll = VkBotLongPoll(vk, 176533270)


while True:
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.object.peer_id == event.object.from_id:
                try:
                    body = event.object.text
                    p = event.object.text.lower()[2:]
                    d = body[0:1]
                    url = 'https://api.github.com/search/repositories?q=language:' + str(p) + '&sort=stars'
                    r = requests.get(url)

                    response_dict = r.json()

                    repo_dicts = response_dict['items']

                    i = 0
                    for repo_dict in repo_dicts:
                        if int(d) >= 6:
                            vk.method("messages.send", {"user_id": event.object.from_id, "message": "Кол-во ссылок не может превышать 5","random_id": 0})
                            break
                        elif i >= int(d):
                            break
                        elif int(d) <= 5:
                            i = i + 1
                            vk.method("messages.send", {"user_id": event.object.from_id, "message":
                                        "\n"
                                        "Имя: " + repo_dict['name'] + "\n" +
                                        "Логин: " + repo_dict['owner']['login'] + "\n" +
                                        "Звёзды: " + str(repo_dict['stargazers_count']) + "\n" +
                                        "Профиль: " + repo_dict['html_url'] + "\n" +
                                        "Создан: " + str(repo_dict['created_at'][0:10]) + "\n" +
                                        "Обновлён: " + str(repo_dict['updated_at'][0:10]) + "\n" +
                                        "Описание: " + repo_dict['description'],
                                                        "random_id": 0})

                            vk.method("messages.send", {"user_id": event.object.from_id, "message": "_________________________________________________________________",
                                                                                        "random_id": 0})
                except:
                    vk.method("messages.send", {"user_id": event.object.from_id, "message": "Вы ввели некорректный запрос","random_id": 0})
