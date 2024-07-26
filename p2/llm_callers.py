import os
from abc import ABC, abstractmethod
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMCaller(ABC):
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt

    @abstractmethod
    def call_llm(self, user_prompt):
        pass

class OpenAICaller(LLMCaller):
    def __init__(self, system_prompt):
        super().__init__(system_prompt)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def call_llm(self, user_prompt):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True
        )
        return ''.join(chunk.choices[0].delta.content or "" for chunk in response)

class GroqCaller(LLMCaller):
    def __init__(self, system_prompt):
        super().__init__(system_prompt)
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def call_llm(self, user_prompt):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        response = self.client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192"
        )
        return response.choices[0].message.content.strip()

# Example usage
if __name__ == "__main__":
    system_prompt = "You are a helpful assistant."
    user_prompt = "Tell me 10 lines Atal Vajpayee."

    openai_caller = OpenAICaller(system_prompt)
    groq_caller = GroqCaller(system_prompt)

    print("OpenAI response:")
    print(openai_caller.call_llm(user_prompt))

    print("\nGroq response:")
    print(groq_caller.call_llm(user_prompt))