from datetime import datetime

import tiktoken


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """
    This function calculates and returns the number of tokens in a given string. The tokenization is based on the
    provided encoding scheme.
    :param string: The input string for which the number of tokens is to be calculated.
    :param encoding_name: The name of the encoding scheme to be used for tokenization.
    :return:
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def write_to_file(text, encoding_name):
    """
    write to file
    :param text:
    :param encoding_name:
    :return:
    """
    timestamp = datetime.now()
    formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    token_count = num_tokens_from_string(text, encoding_name)

    with open('output.txt', 'a', encoding='utf-8') as f:
        f.write(f'{"=============================" * 3}\n')
        f.write(f'Timestamp: {formatted_timestamp}\n')
        f.write(f"Text: '{text}'\n")
        f.write(f"Token Count: {token_count}\n\n")
