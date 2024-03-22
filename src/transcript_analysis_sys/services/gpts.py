import logging

from openai import AsyncOpenAI

from transcript_analysis_sys.config import settings
from transcript_analysis_sys.storages.local import read_text_file
from transcript_analysis_sys.utils.constant import PROMPT_WORDS

client = AsyncOpenAI(
    api_key=settings.API_KEY
)


class GPTS:
    def __init__(self):
        self.temperature = 1
        self.prompts: str = PROMPT_WORDS
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        self.messages = [
            {"role": "system", "content": self.prompts},
        ]

    async def ask(
            self,
            question: str,
            temperature: float = 1
    ):
        """
        ask question
        :param temperature:
        :param question:
        :return:
        """
        new_msg = {
            'role': 'user',
            'content': question
        }
        self.logger.info('New message: %s', new_msg)
        # merge messages
        self.messages.append(new_msg)
        # send message to gpt
        respo = await client.chat.completions.create(
            model=settings.MODEL,
            messages=self.messages,
            temperature=temperature
        )
        _answer = respo.choices[0].message.content
        self.messages.append({'role': 'assistant', 'content': _answer})
        return self.messages

    def update_prompts(self, prompts: str):
        self.prompts = prompts
        self.messages = [
            {"role": "system", "content": self.prompts},
        ]
        return self.prompts

    def update_temperature(self, temperature: float = 1):
        """
        update temperature
        :param temperature:
        :return:
        """
        self.temperature = temperature
        return self.temperature

    async def custom_chat_completions(
            self,
            prompts: str,
            temperature: float,
            content: str,
            name: str
    ):
        """
        custom chat completions
        :param prompts:
        :param temperature:
        :param content:
        :return:
        """
        question = f"""{prompts}. 
New transcript content is as follows: {content}
        """
        new_msg = {
            'role': 'user',
            'content': question
        }
        # merge messages
        self.messages.append(new_msg)
        respo = await client.chat.completions.create(
            model=settings.MODEL,
            messages=self.messages,
            temperature=temperature
        )
        _answer = respo.choices[0].message.content
        self.messages.append({'role': 'assistant', 'content': _answer})
        return self.messages
