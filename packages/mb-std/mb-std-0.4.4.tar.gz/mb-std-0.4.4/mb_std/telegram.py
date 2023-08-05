import time

import pydash

from mb_std import Result, hr, md


def send_telegram_message(bot_token: str, chat_id: int, message: str, long_message_delay=3) -> Result[list[int]]:
    messages = _split_string(message, 4096)
    responses = []
    result = []
    while True:
        text = messages.pop(0)
        res = hr(f"https://api.telegram.org/bot{bot_token}/sendMessage", method="post", params=md(chat_id, text))
        responses.append(res.json)
        if res.is_error():
            return Result.new_error(res.error, {"last_res": res.to_dict(), "responses": responses})  # type:ignore

        message_id = pydash.get(res.json, "result.message_id")
        if message_id:
            result.append(message_id)
        else:
            return Result.new_error("unknown_response", {"last_res": res.to_dict(), "responses": responses})

        if len(messages):
            time.sleep(long_message_delay)
        else:
            break
    return Result.new_ok(result, responses)


def _split_string(text: str, chars_per_string: int) -> list[str]:
    return [text[i : i + chars_per_string] for i in range(0, len(text), chars_per_string)]  # noqa
