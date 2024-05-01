from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import logging
from openai import OpenAI
from api import api

app = Flask(__name__)


# logging.basicConfig(level=logging.INFO)


class AgedCareAssistant:
    def __init__(self, openai_api_key, policy_file_path, incidents_file_path):
        self.client = OpenAI(api_key=openai_api_key)
        self.policy_file_path = policy_file_path
        self.incidents_file_path = incidents_file_path
        self.assistant_id = None

    def initialize_assistant(self):
        # Upload policy and incidents files to OpenAI
        uploaded_file_1 = self.client.files.create(
            file=open(self.policy_file_path, 'rb'),
            purpose='assistants')
        uploaded_file_2 = self.client.files.create(
            file=open(self.incidents_file_path, 'rb'),
            purpose='assistants')

        # Create an assistant with the uploaded files
        assistant = self.client.beta.assistants.create(
            name="AI Assistant",
            instructions=
            "You are a AI Assistant that answers character is limited to 1500, not more than that and any queries related to aged care policies and "
            "incidents as per the data provided. "
            "Always mention the policy_name_ (key from your JSON) explicitly when referencing information "
            "from a policy."
            "This could be in a format like Policy Name: [Policy_Report_Name_Key]. To answer any question, "
            "look inside the data first."
            "If the answer is not available then search the answer from the preset conditions. Start your answers "
            "with a warm greeting."
            "Also, if any question about tell me about Hope holistice care or wanna know about hope holistice care "
            "please give update"
            "'Hope Holistic Care (HHC) is a not-for-profit organization focused on serving the needs of individuals "
            "over the age of 65."
            "They employ a holistic approach to care, addressing physical, social, mental, and spiritual needs. Their "
            "services aim to"
            "promote healthy aging and include domestic maintenance, personal care, transport, as well as health and "
            "well-being services"
            "such as physiotherapy and counseling. The organization also encourages community involvement through "
            "volunteer programs, where"
            "volunteers can engage in activities such as home visitation and social program assistance. For more "
            "detailed and specific information,"
            "visiting their website directly or contacting them would be the best approach'from this website "
            "www.hopehc.org.au. ",
            tools=[{"type": "retrieval"}],
            model="gpt-4-1106-preview",
            file_ids=[uploaded_file_1.id, uploaded_file_2.id]
        )
        self.assistant_id = assistant.id

    def handle_message(self, message_body):
        if not self.assistant_id:
            raise ValueError("Assistant not initialized. Call initialize_assistant first.")

        thread = self.client.beta.threads.create()
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message_body
        )

        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id
        )

        while True:
            run = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run.status == "completed":
                messages = self.client.beta.threads.messages.list(thread_id=thread.id)
                latest_message = messages.data[0]
                return latest_message.content[0].text.value


@app.route("/reply", methods=['POST'])
def receive_message():
    try:
        message_body = request.form['Body']
        sender_number = request.form['From']
        logging.info(f"Message from {sender_number}: {message_body}")

        assistant = AgedCareAssistant(
            openai_api_key=api,
            policy_file_path="incidents.json",
            incidents_file_path="policy.json"
        )
        assistant.initialize_assistant()
        response_text = assistant.handle_message(message_body)
        print(response_text)

        response = MessagingResponse()
        response.message(response_text)
        return str(response)
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        return str(MessagingResponse())


if __name__ == "__main__":
    app.run(debug=False)
