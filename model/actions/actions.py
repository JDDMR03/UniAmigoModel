# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Define el primer mensaje que enviara el chatbot
class ActionSessionStart(Action):

    def name(self) -> Text:
        return "action_session_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="¡Hola! Soy UniAmigo, un chatbot desarrollado por TigresTech.\nEstoy aquí para proporcionarte información sobre la UANL. Puedo ayudarte con los siguientes temas:\n \n1. Ubicación de la UANL.\n2. Ubicaciones más importantes de la UANL.\n3. Horario de Escolar\n4. Facultades que tiene la UANL.\n \n¿Hay algo que quisieras conocer?")

        return []

# Verifica si hay una expresion o palabra inapropiada
class ActionDetectaPalabrasProhibidas(Action):

    def name(self) -> Text:
        return "action_detectar_palabras_prohibidas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Obtiene las entidades detectadas por el tracker
        entities = tracker.latest_message.get('entities', [])

        for entity in entities:
            if entity['entity'] == 'palabras_prohibidas':
                palabra_prohibida = entity['value'].lower()

                # Verifica si la palabra prohibida esta en el input del usuario
                input_usuario = tracker.latest_message.get('text', '').lower()

                if palabra_prohibida in input_usuario:
                    dispatcher.utter_message(text=f"Por favor, no uses la palabra/expresión '{palabra_prohibida}' en esta conversación, ya que no esta permitido decir groserias o cosas inapropiadas.")
                    return []

        return []
    
# Se envia un mensaje si el chatbot no puede entender la intencion del usuario
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Lo siento, no entiendo a que te refieres.")
        return [] 