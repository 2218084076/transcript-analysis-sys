import copy
import logging
import time
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, File, Form, UploadFile

# from transcript_analysis_sys.services.gpts import GPTS
from transcript_analysis_sys.services.groq import GroqChatBot
from transcript_analysis_sys.storages.local import LocalStorages
from transcript_analysis_sys.utils.constant import TIMESTAMP_FORMAT
from transcript_analysis_sys.utils.message import Message
from transcript_analysis_sys.utils.stt import STT
from transcript_analysis_sys.utils.utils import process_messages

_base_dir = Path(__file__).parent.parent

logger = logging.getLogger(f'{__name__}  {__name__}')
gpt = GroqChatBot()
stt = STT()
file = LocalStorages()
router = APIRouter()
all_messages = []


@router.get('/')
async def hello_world():
    """
    hello world
    :return:
    """
    return Message(
        message='Hello World',
    )


@router.post('/chatCompletion/')
async def chat_completion(
        content: str = Form(),
        temperature: float = Form()
):
    """
    chat completion
    :param content:
    :param temperature:
    :return:
    """
    start_time = time.time()
    res = await gpt.ask(
        # temperature=float(temperature) or 1,
        question=content
    )
    _msg = copy.deepcopy(res)
    all_messages.extend(_msg[-2:])
    return Message(
        message='Chat completion successful',
        data=all_messages,
        response_time=time.time() - start_time,
    )


@router.post('/analyse/')
async def analyse(
        audio: UploadFile = File(),
        temperature: float = Form(),
        content: str = Form()
):
    """
    chat completion
    :param content:
    :param audio:
    :param temperature:
    :return:
    """
    current_time = datetime.now()
    start_time = time.time()
    # save audio file
    save_path = _base_dir / 'input' / f'{current_time.strftime(TIMESTAMP_FORMAT)}' / 'ask.wav'
    save_path.parent.mkdir(parents=True, exist_ok=True)
    data = await audio.read()
    await file.save(save_path, data)
    # stt transcribe audio
    audio_content = await stt.transcribe_audio(save_path)
    # chat gpt step
    res = await gpt.custom_chat_completions(
        question=content,
        audio_content=audio_content,
        temperature=temperature or 1,
    )
    all_messages.extend(res[-2:])
    processed_messages = process_messages(all_messages)
    return Message(
        message='Chat completion successful',
        data=processed_messages,
        response_time=time.time() - start_time,
    )


@router.get('/temperature/')
def get_temperature():
    """
    get temperature
    :return:
    """
    return gpt.temperature


@router.post('/temperature/')
def update_temperature(
        temperature: float = Form(description='Modify temperature')
):
    """
    Modify temperature
    :param temperature:
    :return:
    """
    return gpt.update_temperature(temperature)


@router.get('/prompts/')
def get_prompt():
    """
    get prompt
    :return:
    """
    return gpt.prompts


@router.post('/prompts/')
def update_prompt(
        prompt: str = Form(description='Modify prompts')
):
    """
    Modify prompts
    :param prompt:
    :return:
    """
    return gpt.update_prompts(prompt)


@router.get('/messages/')
def get_messages():
    return all_messages


@router.get('/initMessages/')
def init_messages():
    """
    init messages
    :return:
    """
    global all_messages
    all_messages = [
    ]
    gpt.init_messages_context()
