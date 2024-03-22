import logging

from groq import AsyncGroq

from transcript_analysis_sys.config import settings
from transcript_analysis_sys.utils.constant import PROMPT_WORDS

client = AsyncGroq(
    api_key=settings.GROQ_API_KEY
)


class GroqChatBot:
    """chatbot based on groq"""
    model = settings.GROQ_MODEL or 'mixtral-8x7b-32768'

    def __init__(self):
        self.temperature: float = 0.7
        self.prompts: str = PROMPT_WORDS
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        self.messages = [
            {"role": "system", "content": self.prompts},
        ]

    async def ask(self, question: str):
        """
        ask
        :param question:
        :return:
        """
        new_msg = {
            'role': 'user',
            'content': question
        }
        self.logger.info('New message: %s', new_msg)
        self.messages.append(new_msg)
        respo = await client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            temperature=self.temperature,
            max_tokens=32768,
            top_p=1,
            stop=None,
            stream=False,
            timeout=120
        )
        _answer = respo.choices[0].message.content
        self.messages.append({'role': 'assistant', 'content': _answer})
        return self.messages

    async def custom_chat_completions(
            self,
            question: str,
            temperature: float = 1,
            audio_content: str = ''
    ):
        """
        chat completions
        :param audio_content:
        :param temperature:
        :param question:
        :return:
        """
        question = f"""{question}. 
        New transcript content is as follows: {audio_content}
                """
        new_msg = {
            'role': 'user',
            'content': question
        }
        self.messages.append(new_msg)

        chat_comp = await client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            temperature=temperature,
            max_tokens=32768,
            top_p=1,
            stop=None,
            stream=False,
            timeout=120
        )
        self.messages[-1].update(chat_comp)
        _answer = chat_comp.choices[0].message.content
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

    def init_messages_context(self):
        """
        init messages context
        :return:
        """
        self.messages = [
            {"role": "system", "content": self.prompts},
        ]
