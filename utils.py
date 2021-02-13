from gnewsclient import gnewsclient
import dialogflow_v2 as dialogflow
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client.json"


client = gnewsclient.NewsClient()

dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "newsbot-amgr"


def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(
        session=session, query_input=query_input)
    return response.query_result


def get_reply(query, chat_id):
    response = detect_intent_from_text(query, chat_id)

    if response.intent.display_name == "get_news":
        return "get_news", dict(response.parameters)
    else:
        return "small_talk", response.fulfillment_text


def fetch_news(parameters):
    client.language = parameters['language']
    client.location = parameters['geo-country']
    if parameters['topic']:
        client.topic = parameters['topic'][0]
    else:
        client.topic = 'World'
    return client.get_news()[:5]


topics_keyboard = [
    ['World', 'Nation', 'Health'],
    ['Business', 'Technology', 'Entertainment'],
    ['Sports', 'Science'],
]
