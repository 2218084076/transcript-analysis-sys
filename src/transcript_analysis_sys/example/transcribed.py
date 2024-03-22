import logging
from pathlib import Path

import requests

from transcript_analysis_sys.utils.log import init_log

STT_URL = "http://lab.tfg.ai:12100/recognition"

logger = logging.getLogger(f'{__name__}')


def transcribe_audio(audio_file_path):
    """
    Transcribe audio synchronously using requests.
    """
    with open(audio_file_path, 'rb') as audio_file:
        files = {'audio': (audio_file_path.name, audio_file, 'audio/mp3')}
        data = {"to_simple": 0, "remove_pun": 0, "task": "transcribe"}
        response = requests.post(url=STT_URL, files=files, data=data)
    if response.ok:
        res_data = response.json()
        return ''.join([item['text'] for item in res_data['results']])
    logger.info('%s content is "%s"', audio_file, ' ')
    return ''


def process_directory(directory_path):
    for audio_file_path in Path(directory_path).glob('*/*.mp3'):
        logger.info(audio_file_path)
        transcription = transcribe_audio(audio_file_path)
        txt_file_path = audio_file_path.parent / 'Whisper-Finetune.txt'
        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(transcription)
        logger.info("完成转录: %s -> %s", audio_file_path, txt_file_path)


if __name__ == '__main__':
    init_log()
    directory_path = r'D:\Terry\develop\tfg\transcript-analysis-sys\ai-recording'
    process_directory(directory_path)
    # transcribe_audio(Path(r"D:\Terry\develop\tfg\transcript-analysis-sys\ai-recording\64081538\64081538.mp3"))
