import logging

ex = 'Audio transcription failed.'
logger = logging.getLogger(f'{__name__}')


def process_messages(all_messages):
    processed_messages = []

    for message in all_messages:
        if message['role'] == 'user':
            content = message['content']
            if ex in content:
                logger.info('Audio transcription failed')
                continue
            indicator = 'New transcript content is as follows:'
            index = content.find(indicator)
            if index != -1:
                # 如果找到了字符串，计算indicator结束的索引位置
                start_index = index + len(indicator)
                # 保留indicator之后的3个字符
                after_indicator = content[start_index:start_index + 14]
                # 获取内容的最后3个字符
                last_three_chars = content.strip()[-10:]
                # 拼接结果
                message['content'] = f"{content[:start_index]}{after_indicator} ***** {last_three_chars}"
            processed_messages.append(message)
        else:
            processed_messages.append(message)

    return processed_messages
