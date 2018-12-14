"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import requests
from random import randint


def get_weather(city_name):
    city_of_interest = city_name
    r = requests.get('https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}'
                     .format(city_of_interest, "e3b24d902d335691023a8b85fe0f6f00"))
    weather_request_content = json.loads(r.content)
    city_temp = (weather_request_content['main']['temp'])
    city_humidity = (weather_request_content['main']['humidity'])
    weather_desc = (weather_request_content['weather'][0]['description'])
    return city_temp


def get_news(interest):
    string = interest
    r = requests.get('https://newsapi.org/v2/everything?q={}&apiKey=76df204fc60d4002b08c5d6f7bef8606'.format(string))
    r_to_object = json.loads(r.content)
    random_headline = randint(0, 2)
    return r_to_object['articles'][random_headline]['title']


def get_quote(mood):
    # "contents": {
    #     "categories": {
    #         "inspire": "Inspiring Quote of the day",
    #         "management": "Management Quote of the day",
    #         "sports": "Sports Quote of the day",
    #         "life": "Quote of the day about life",
    #         "funny": "Funny Quote of the day",
    #         "love": "Quote of the day about Love",
    #         "art": "Art quote of the day ",
    #         "students": "Quote of the day for students"
    #         "students": "Quote of the day for students"
    #     },
    # }
    string = mood
    r = requests.get('http://quotes.rest/qod.json?category={}'.format(string))
    r_to_object = json.loads(r.content)
    return r_to_object['contents']['quotes'][0]['quote']


def get_trumps_opinion(subject):
    trump_opinion_on = subject
    r = requests.get('https://api.tronalddump.io/search/quote?query={}'.format(trump_opinion_on))
    r_to_object = json.loads(r.content)
    return r_to_object["_embedded"]['quotes'][0]['value']


def get_joke(team_name):
    r = requests.get('https://api.chucknorris.io/jokes/random')
    r_to_object = json.loads(r.content)
    return r_to_object['value']


def get_name_response(name):
    return "ok {}, what can I do you for?".format(name)


def check_if_received_name(message):
    possible_name_announcements = ["my name is", "i am called", "i go by", "you can call me", "is my name",
                                   "my nickname is", "call me", "you may refer to me as"]
    message_list = message.split()
    if len(message_list) < 8:
        if any(name_decleration in message.lower() for name_decleration in possible_name_announcements):
            for i in range(len(possible_name_announcements)):
                if possible_name_announcements[i] in message.lower():
                    name = message.lower().replace(possible_name_announcements[i], '')
                    return name
        else:
            return False
    else:
        return False


def get_greeting():
    hello_responses = ["Hi! What is your name my homie?", "Oh hello back to you! What name did your mother give you?",
                       "Hey! What are you called in the streets?"]
    i = randint(0, 2)
    return hello_responses[i]


def check_if_greeting(message):
    possible_greetings = ["hi ", "hello ", "good morning ", "good afternoon ", "good evening ", "hola ", "shalom ", "greetings "]
    possible_nospaces_greetings = ["hi", "hello", "good morning", "good afternoon", "good evening", "hola", "shalom", "greetings"]
    if len(message.split()) > 3:
        for i in range(len(possible_greetings)):
            if possible_greetings[i] in message.lower():
                index_of_greeting = message.split().index(possible_nospaces_greetings[i])
                if index_of_greeting > 4:
                    return False
                else:
                    if any(greeting in message.lower() for greeting in possible_greetings):
                        return True
                    else:
                        return False
    else:
        if any(greeting in message.lower() for greeting in possible_nospaces_greetings):
            return True
        else:
            return False


def routing_incoming_statement(message):
    # city_temp = get_weather(message)
    # joke = get_joke(message)
    # news = get_news(message)
    # quote = get_quote(message)
    # trump_opinion = get_trumps_opinion(message)

    greeting_bool = check_if_greeting(message)
    if greeting_bool:
        return get_greeting()

    name = check_if_received_name(message)
    print(name)
    if name != False:
        print("went to get name")
        return get_name_response(name)


def selecting_animation(message):
    return "inlove"


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')

    return json.dumps({"animation": selecting_animation(user_message), "msg": routing_incoming_statement(user_message)})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
