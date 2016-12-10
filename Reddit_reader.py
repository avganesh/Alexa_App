from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode 

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")


def get_headlines(topic):
    user_pass_dict = {'user': 'AlexaAppThrowaway',
                      'passwd': 'password',
                      'api_type': 'json'}
    topic_to_reddit_dict = {'Donald': 'the_donald',
                      'Finance': 'finance',
                      'Tech': 'technology',
                      'Clop':'clopclop',
                      'World': 'worldnews'
                            }
    if (not (topic in topic_to_reddit_dict)):
        topic = 'Donald'

    redditPath = topic_to_reddit_dict[topic]

    sess = requests.Session()
    sess.headers.update({'User-Agent': 'I am testing Alexa: AlexaAppThrowaway'})
    sess.post('https://www.reddit.com/api/login', data = user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/{}/top/.json?limit=10'.format(redditPath)
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
    titles = '... '.join([i.replace("Trump", "Nitish") for i in titles])
    return titles


@app.route('/')
def homepage():
##    return "Hi there, how ya doin? -- latest code"
    return get_headlines('Tech')

@ask.launch
def start_skill():
    welcome_message = 'What the fuck do you want Nitish, do you want to hear the news? ... ... ... Bitch.'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines(NewsTopic):
    headlines = get_headlines(NewsTopic)
    headline_msg = 'You want to know about the fucking {} ok... bitch.. the current fucking headlines are {}'.format(NewsTopic, headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... ... bye forever'
    return statement(bye_text)


if __name__ == '__main__':
    port = 5000 
    app.run(host='0.0.0.0', port=port, debug=True)
