# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

class ActionSessionStart(Action):

    def name(self) -> Text:
        return "action_session_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="¡Hola! Soy UniAmigo, un chatbot desarrollado por TigresTech.\n\nEstoy aquí para proporcionarte información sobre la UANL. Puedo ayudarte con los siguientes temas:\n\n1. Ubicación de la UANL. \n2. Ubicaciones más importantes de la UANL. \n3. Horario de Escolar \n4. Facultades que tiene la UANL. \n\n¿Hay algo que quisieras conocer?")

        return []
