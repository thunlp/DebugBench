import os
import time
import openai
from abc import ABC, abstractmethod


class Responser(ABC):

    @abstractmethod
    def respond(self, system_info: str, user_prompt: str) -> str:
        pass


class GPT4Responser(Responser):
    """ Openai LLM responser """

    def __init__(self, model='gpt-4'):
        """ environment information """
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        openai.api_base = os.environ.get("OPENAI_API_BASE")
        openai.api_type = 'azure'
        openai.api_version = '2023-07-01-preview'
        self.model = model

    def respond(self, system_info: str, user_prompt: str) -> str:
        """
        respond to system_info and user prompt
        :param system_info: see in openai documentation
        :param user_prompt: see in openai documentation
        :return: response in form of string
        """
        try:
            response = openai.ChatCompletion.create(
                engine=self.model,
                messages=[
                    {"role": "system", "content": system_info},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=2000,
                stop=None,
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(f"{e}\nRate Limit Reached! Sleeping for 20 secs...")
            time.sleep(20)
            response = openai.ChatCompletion.create(
                engine=self.model,
                messages=[
                    {"role": "system", "content": system_info},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=2000,
                stop=None,
            )
            return response['choices'][0]['message']['content']


class TurboResponser(Responser):
    """ Openai LLM responser """

    def __init__(self, model='gpt-3-turbo'):
        """ environment information """
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        openai.api_base = os.environ.get("OPENAI_API_BASE")

    def respond(self, system_info: str, user_prompt: str) -> str:
        """
        respond to system_info and user prompt
        :param system_info: see in openai documentation
        :param user_prompt: see in openai documentation
        :return: response in form of string
        """
        messages = [
            {"role": "system", "content": system_info},
            {"role": "user", "content": user_prompt}
        ]
        response = openai.ChatCompletion.create(
            # model='gpt-4',
            model='gpt-3.5-turbo',
            # model='gpt-4-32k',
            # model='gpt-3.5-turbo-16k',
            messages=messages
        )
        return response['choices'][0]['message']['content']


if __name__ == '__main__':
    # gpt4_responser = GPT4Responser()
    turbo_responser = TurboResponser()
    print(turbo_responser.respond(system_info="Translate the text into English",
                                  user_prompt=f"El presidente de la República, Andrés Manuel López Obrador"))
