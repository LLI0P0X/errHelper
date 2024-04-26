import textwrap
import requests

import config
import json
import traceback
import sys


class Helper():
    def __init__(self,
                 token: str | None = None,
                 fill: int = 120,
                 frequency_penalty: int = 0,
                 max_tokens: int = 2048,
                 presence_penalty: int = 0,
                 stop: None = None,
                 stream: bool = False,
                 temperature: int = 1,
                 top_p: int = 1):
        if token is str:
            self.DeepSeekAPIToken = token
        else:
            try:
                import config
                self.DeepSeekAPIToken = config.DeepSeekAPIToken
            except AttributeError | ModuleNotFoundError:
                raise 'you must pass the token when creating the class or have a DeepSeekAPIToken variable in config.py'
        self.fill = fill
        self.frequency_penalty = frequency_penalty
        self.max_tokens = max_tokens
        self.presence_penalty = presence_penalty
        self.stop = stop
        self.stream = stream
        self.temperature = temperature
        self.top_p = top_p

    def askDSC_AI(self, err: str):
        url = "https://api.deepseek.com/v1/chat/completions"

        payload = json.dumps({
            "messages": [
                {
                    "content": "Ты объясняешь причины присланных ошибок и предлагаешь варианты решения этих ошибок на русском языке",
                    "role": "system"
                },
                {
                    "content": f'Объясни причину ошибки и напиши варианты ее решения\n{err}',
                    "role": "user"
                }
            ],
            "model": "deepseek-coder",
            "frequency_penalty": self.frequency_penalty,
            "max_tokens": self.max_tokens,
            "presence_penalty": self.presence_penalty,
            "stop": self.stop,
            "stream": self.stream,
            "temperature": self.temperature,
            "top_p": self.top_p
        })

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.DeepSeekAPIToken}'
        }

        resp = requests.post(url, headers=headers, data=payload)
        ans = str(resp.json()['choices'][0]['message']['content'])

        if self.fill:
            for q in ans.split('\n'):
                print(textwrap.fill(q, self.fill))
        else:
            print(ans)


if __name__ == '__main__':
    try:
        q = 1 / 0
    except Exception as err:
        traceback.print_exception(err, file=sys.stdout)
        tr = ['y', 'yes', 'д', 'да']
        ans = input(f'\nСпростить об ошибке у DeepSeek code? ({tr})\n')
        if ans in tr:
            print('\nОжидание ответа от ии...\n')
            try:
                helper = Helper()
            except:
                helper = Helper(config.DeepSeekAPIToken)  # заменить config.DeepSeekAPIToken на "Ваш api токен"
            helper.askDSC_AI(str(traceback.format_exc()))
        print('\nУдачи)')
