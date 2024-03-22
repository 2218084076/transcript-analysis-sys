import asyncio
import logging
from pathlib import Path

_base_dir = Path(__file__).parent.parent.parent
logger = logging.getLogger(f'{__name__}')


class LocalStorages:
    """Local storage"""

    def __init__(self):
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    async def save(self, save_file, data):
        """
        save file
        :param save_file:
        :param data:
        :return:
        """
        await asyncio.to_thread(self.write_to_file, save_file, data)
        return save_file

    def write_to_file(self, file, data):
        """write to file"""
        with open(file, 'wb') as obj:
            obj.write(data)
        self.logger.info('Save file to %s.', file)


def read_text_file(filename: str):
    """
    read text file
    :param filename:
    :return:
    """
    logger.info(_base_dir / 'input' / filename / 'original.txt')
    with open(
            _base_dir / 'input' / filename / 'original.txt',
            'r',
            encoding='utf-8'
    ) as file:
        new = file.read()
        return new
