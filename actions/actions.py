from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionAskForPart(Action):
    def name(self) -> str:
        return "action_ask_for_part"  # Custom action name

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="What parts are you checking compatibility for?")
        return []

class ActionGoodbye(Action):
    def name(self) -> str:
        return "action_goodbye"  # Custom action name

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="Goodbye! Have a great day!")
        return []

class ActionIAmABot(Action):
    def name(self) -> str:
        return "action_iamabot"  # Custom action name

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="I am a bot, created to help you with product compatibility.")
        return []



class ActionCheckCompatibility(Action):

    def name(self) -> Text:
        return "action_check_compatibility"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # load the csv file
        compatibility_data = pd.read_csv("hardware_compatibility.csv")

        # get the user message
        user_message = tracker.latest_message.get("text").strip().lower()

        # search for the users  product in the csv
        matching_product = compatibility_data[compatibility_data['Product_Name'].str.lower() == user_message]

        if not matching_product.empty:
            product_type = matching_product.iloc[0]['Product_Type']
            product_name = matching_product.iloc[0]['Product_Name']
            features = matching_product.iloc[0]['Features']
            compatible_with = matching_product.iloc[0]['Compatible_With']
            response = (
                f"The {product_type} '{product_name}' has the following features: {features}.\n"
                f"It is compatible with: {compatible_with}."
            )
        else:
            response = "I'm sorry, I couldn't find compatibility information for that product. Please try again."

        dispatcher.utter_message(text=response)
        return []
