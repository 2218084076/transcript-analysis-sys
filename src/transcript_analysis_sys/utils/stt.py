import asyncio
import logging

import httpx

from transcript_analysis_sys.config import settings


class STT:
    """Speech to Text"""
    STT_URL = settings.STT_URL

    def __init__(self):
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    async def transcribe_audio(self, audio_file):
        """
        transcribe audio asynchronously using httpx

        The parameters when requesting the `stt api` interface are as follows:
            - audio: Audio File
            - to_simple: Traditional Chinese to Simplified Chinese
            - remove_pun: Whether to remove punctuation
            - task: Identify task types and support transcribe and translate
            - language: Set the language, shorthand, to automatically detect the language if None
        :param audio_file:
        :return:
        """
        files = {'audio': (audio_file.name, open(audio_file, 'rb'), 'audio/wav')}
        data = {"to_simple": 0, "remove_pun": 0, "task": "transcribe"}
        try:
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(
                    url=self.STT_URL,
                    files=files,
                    data=data
                )
            res_data = response.json()
            content = ''.join([item['text'] for item in res_data['results']])
            await asyncio.to_thread(self.save_original, content, audio_file.parent)
            return content
        except Exception as ex:
            self.logger.warning('Audio transcription failed, error: %s', ex)
            return f'Audio transcription failed.\n{ex}'

    def save_original(self, content: str, folder):
        """
        save original text
        :param content:
        :param folder:
        :return:
        """
        self.logger.info('save original %s', folder/'original.txt')
        with open(folder / 'original.txt', 'w', encoding='utf-8') as file:
            file.write(content)
