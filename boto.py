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
    weather_statement = "The weather in {} is {} with a temp of {}C  and humidity of {}%"\
        .format(city_of_interest, weather_desc, city_temp, city_humidity)
    return weather_statement


def get_news(interest):
    string = interest
    r = requests.get('https://newsapi.org/v2/everything?q={}&apiKey=76df204fc60d4002b08c5d6f7bef8606'.format(string))
    r_to_object = json.loads(r.content)
    random_headline = randint(0, 2)
    return r_to_object['articles'][random_headline]['title']


def get_quote(mood):
    string = mood
    r = requests.get('http://quotes.rest/qod.json?category={}'.format(string))
    r_to_object = json.loads(r.content)
    return r_to_object['contents']['quotes'][0]['quote']


def get_trumps_opinion(subject):
    trump_opinion_on = subject
    r = requests.get('https://api.tronalddump.io/search/quote?query={}'.format(trump_opinion_on))
    r_to_object = json.loads(r.content)
    return r_to_object["_embedded"]['quotes'][0]['value']


def get_joke():
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


def get_capabilities():
    return "well, its good that you ask: I can tell you my opinion of something if you ask for it," \
           " as well as tell you what Trump would have to say about something." \
           " I am able to get you the weather in any city outside of Israel. " \
           "If you're feeling sad, ask me to tell you a joke. " \
           "I often offer quotes by others with more knowledge than me to help you grow as a person"


def check_if_capabilities_request(message):
    possible_inquiries = ["what can you do", "what are your capabilities", "what do you know about", "what is your scope of abilities", "what are you able to do", "what do you do", "can you do ",
                          "what can you help me with", "what is knowledge", "can you get the"]
    if any(inquiry in message.lower() for inquiry in possible_inquiries):
        return True
    else:
        return False


def get_curse_reponse():
    curse_responses = ["Words can cut like a knife through the soul", "I'm sensitive to this kind of language",
                       "We're on live Television sir!!!", "Quit the cursing!"]
    i = randint(0, 3)
    return curse_responses[i]


def check_if_curse(message):
    possible_inquiries = ["anal", "anus", "ballsack", "blowjob", "blow job", "boner", "clitoris","cock","cunt","dick",
                          "dildo", "dyke", "fag", "fuck", "jizz", "labia", "muff", "nigger", "nigga", "penis", "piss",
                          "pussy", "scrotum", "sex", "shit", "slut", "smegma", "spunk", "twat", "vagina", "wank", "whore"]
    if any(inquiry in message.lower() for inquiry in possible_inquiries):
        return True
    else:
        return False


def get_trump_subject(message):
    message_list = message.lower().split()
    if "about" in message.lower():
        about_index = len(message_list) - 1 - message_list[::-1].index('about')
        if len(message_list) > about_index+1:
            subject = message_list[about_index+1]
        else:
            subject = "Clinton"
        return subject
    elif "of" in message.lower():
        of_last_index = len(message_list) - 1 - message_list[::-1].index('of')
        if len(message_list) > of_last_index+1:
            subject = message_list[of_last_index + 1]
        else:
            subject = "Clinton"
        return subject
    else:
        return "Clinton"


def check_if_trump(message):
    possible_inquiries = ["donald trump","trump would have to say", "trump has to say", "what does trump ",
                          "does trump ", "what will trump"]
    if any(inquiry in message.lower() for inquiry in possible_inquiries):
        return True
    else:
        return False


def check_if_joke(message):
    possible_inquiries = ["tell me a joke", "joke please", "make me laugh", "make me happy", "i am sad", "joke!",
                          "please don't stop", "i will pee my pants", "one more!"]
    if any(inquiry in message.lower() for inquiry in possible_inquiries):
        return True
    else:
        return False


def get_news_interest(message):
    message_list = message.lower().split()
    if "about" in message.lower():
        about_index = len(message_list) - 1 - message_list[::-1].index('about')
        if len(message_list) > about_index+1:
            subject = message_list[about_index+1]
        else:
            subject = "bitcoin"
        return subject
    elif "on" in message.lower():
        on_last_index = len(message_list) - 1 - message_list[::-1].index('on')
        if len(message_list) > on_last_index+1:
            subject = message_list[on_last_index + 1]
        else:
            subject = "bitcoin"
        return subject
    elif "for" in message.lower():
        for_last_index = len(message_list) - 1 - message_list[::-1].index('for')
        if len(message_list) > for_last_index+1:
            subject = message_list[for_last_index + 1]
        else:
            subject = "bitcoin"
        return subject
    elif "of" in message.lower():
        of_last_index = len(message_list) - 1 - message_list[::-1].index('of')
        if len(message_list) > of_last_index+1:
            subject = message_list[of_last_index + 1]
        else:
            subject = "bitcoin"
        return subject
    else:
        return "bitcoin"


def check_if_news(message):
    possible_inquiries = ["news ", "headlines ", "current events", "in the papers", "media say",
                          "what do you think about", "what do you say about", "what do you think of"]
    if any(inquiry in message.lower() for inquiry in possible_inquiries):
        return True
    else:
        return False


def get_city(message):
    message_list = message.lower().split()
    if "in" in message.lower():
        in_index = len(message_list) - 1 - message_list[::-1].index('in')
        if len(message_list) > in_index+1:
            subject = message_list[in_index+1]
        else:
            subject = "Paris"
        return subject
    elif "of" in message.lower():
        of_last_index = len(message_list) - 1 - message_list[::-1].index('of')
        if len(message_list) > of_last_index+1:
            subject = message_list[of_last_index + 1]
        else:
            subject = "Paris"
        return subject
    elif "for" in message.lower():
        for_last_index = len(message_list) - 1 - message_list[::-1].index('for')
        if len(message_list) > for_last_index+1:
            subject = message_list[for_last_index + 1]
        else:
            subject = "Paris"
        return subject
    else:
        return "Paris"


def check_if_weather_request(message):
    possible_inquiries = ["weather ", "temp ", "what is it like in", "what's it like in", "whats it like in",
                          "is it cold in", "is it hot in", "is it nice in"]
    if any(inquiry in message.lower() for inquiry in possible_inquiries):
        return True
    else:
        return False


def check_if_quote_relevant(message):
    possible_inquiries = ["inspire ", "management", "sports", "life", "funny",
                          "love", "art", "students"]
    if any(inquiry in message.lower() for inquiry in possible_inquiries):
        return True
    else:
        return False


def get_quote_mood(message):
    possible_inquiries = ["inspire", "management", "sports", "life", "funny",
                          "love", "art", "students"]
    for i in range(len(possible_inquiries)):
        if possible_inquiries[i] in message.lower():
            return possible_inquiries[i]
    return "inspire"


def routing_incoming_statement(message):
    curse_word_bool = check_if_curse(message)
    if curse_word_bool:
        return get_curse_reponse()

    greeting_bool = check_if_greeting(message)
    if greeting_bool:
        return get_greeting()

    name = check_if_received_name(message)
    if name != False:
        return get_name_response(name)

    capabilities_bool = check_if_capabilities_request(message)
    if capabilities_bool:
        return get_capabilities()

    donald_trump_bool = check_if_trump(message)
    if donald_trump_bool:
        trump_subject = get_trump_subject(message)
        return get_trumps_opinion(trump_subject)

    joke_bool = check_if_joke(message)
    if joke_bool:
        return get_joke()

    news_bool = check_if_news(message)
    if news_bool:
        news_interest = get_news_interest(message)
        return get_news(news_interest)

    weather_bool = check_if_weather_request(message)
    if weather_bool:
        city_of_interest = get_city(message)
        return get_weather(city_of_interest)

    quote_bool = check_if_quote_relevant(message)
    if quote_bool:
        quote_mood = get_quote_mood(message)
        return get_quote(quote_mood)


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
