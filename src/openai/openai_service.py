import openai
from src.openai.openai_config import *
import threading
import queue
import time

# Product knowledge
product_info = {
        'product_name': 'Apple iPhone 13',
        'description': 'The iPhone 13, released by Apple in September 2021, represents the latest iteration of the iconic smartphone series. Boasting a refined design, it features a Super Retina XDR display available in four sizes: iPhone 13 mini, iPhone 13, iPhone 13 Pro, and iPhone 13 Pro Max. Equipped with the powerful A15 Bionic chip, it offers improved performance and efficiency compared to its predecessors. The iPhone 13 lineup introduces advancements in camera technology, including enhanced low-light performance, sensor-shift optical image stabilization, and improved computational photography capabilities. Additionally, it offers longer battery life, 5G connectivity, and various software enhancements, making it a compelling choice for users seeking cutting-edge features and performance in a premium smartphone.',
        'features': ['Advanced Camera System', 'A15 Bionic Chip', 'Super Retina XDR Display'],
        'pricing': 'iPhone 13 mini: Starting at around $699 for the base model with 128GB of storage., iPhone 13: Starting at around $799 for the base model with 128GB of storage., iPhone 13 Pro: Starting at around $999 for the base model with 128GB of storage., iPhone 13 Pro Max: Starting at around $1,099 for the base model with 128GB of storage.',
}


# Initial chat prompt

class Openai_Service:

    chat_history = []

    def __init__(self):
        openai.api_key = api_key
        self.product_info = product_info
        self.chat_history = []
        self.user_input_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.chat_thread = threading.Thread(target=self.chat_loop)


    def start_chat(self):
        self.chat_thread.start()
        while not self.stop_event.is_set():
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                self.stop_event.set()
            else:
                self.user_input_queue.put(user_input)

    def chat_loop(self):
        print(f"Sales Bot: Hello! Welcome to {self.product_info['product_name']} support. How can I assist you today?")
        while not self.stop_event.is_set():
            try:
                user_input = self.user_input_queue.get(timeout=1)  # Check for new input every second
                self.chat_history.append(f"User: {user_input}")
                response = self.generate_response(user_input)
                self.chat_history.append(f"Sales Bot: {response}")
                print(f"Sales Bot: {response}")
            except queue.Empty:
                pass
            time.sleep(0.1)

    def generate_response(self, user_input):
        prompt = self.construct_prompt(user_input)
        response = self._generate_response(prompt)
        return response

    def construct_prompt(self, user_input):
        prompt = f"{self.product_info['product_name']} Support\n"
        prompt += f"{self.product_info['description']}\n"
        prompt += f"Features: {', '.join(self.product_info['features'])}\n"
        prompt += f"Pricing: {self.product_info['pricing']}\n\n"
        prompt += f"User: {user_input}\n"
        prompt += '\n'.join(self.chat_history)  # Include all chat history without the user input
        return prompt


    def _generate_response(self,prompt):
        response = openai.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=150,
                temperature=0.7,
                n=1)
        print(response)
        return response.choices[0].text.strip()

    if __name__ == "__main__":
        chatbot()
