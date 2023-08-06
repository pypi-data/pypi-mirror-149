import os
from ._vars import _BASE_URL
import requests as _requests
from .errors import BadRequestError as _BadRequestError, UrlNotFoundError as _UrlNotFoundError, \
    UnauthorizedError as _UnauthorizedError, ServiceUnavailableError as _ServiceUnavailableError, \
    InvalidPath as _InvalidPath


class CustomServer:
    def __init__(self, bot_token: str) -> None:
        self.BOT_TOKEN: str = bot_token

    def upload(self, file_path, channel_id) -> str:
        with open(file_path, mode='rb') as file:
            r = _requests.post(
                url=_BASE_URL + '/file/upload',
                headers={'bot_token': self.BOT_TOKEN},
                data={
                    'channel_id': channel_id,
                },
                files={
                    'file': file
                }
            )

        if r.status_code == 200:
            return r.json()['file_key']

        elif r.status_code == 400:
            raise _BadRequestError()

        elif r.status_code == 401:
            raise _UnauthorizedError()

        elif r.status_code == 404:
            raise _UrlNotFoundError()

        elif r.status_code == 503:
            raise _ServiceUnavailableError()

    def download(self, file_key: str, save_path: str) -> None:
        if not os.path.isfile(save_path):
            raise _InvalidPath()

        r = _requests.post(
            url=_BASE_URL + '/file/download',
            headers={'bot_token': self.BOT_TOKEN},
            data={
                'file_key': file_key,
            }
        )
        if r.status_code == 200:
            with _requests.get(r.text, stream=True) as r:
                r.raise_for_status()
                with open(save_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

        elif r.status_code == 400:
            raise _BadRequestError()

        elif r.status_code == 401:
            raise _UnauthorizedError()

        elif r.status_code == 404:
            if r.json()['error']['message'] == "File Not Found":
                raise FileNotFoundError(f"The file with key \"{file_key}\" doesn't exists")
            if r.json()['error']['message'] == "URL Not Found":
                raise _UrlNotFoundError()

        elif r.status_code == 503:
            raise _ServiceUnavailableError()

    def edit(self, file_key: str, file_path: str) -> str:
        if not os.path.isfile(file_path):
            raise _InvalidPath()

        with open(file_path, mode='rb') as file:
            r = _requests.post(
                url=_BASE_URL + '/file/edit',
                headers={'bot_token': self.BOT_TOKEN},
                data={'file_key': file_key},
                files={
                    'file': file
                }
            )

        if r.status_code == 200:
            return r.json()['file_key']

        elif r.status_code == 400:
            raise _BadRequestError()

        elif r.status_code == 401:
            raise _UnauthorizedError()

        elif r.status_code == 404:
            if r.json()['error']['message'] == "File Not Found":
                raise FileNotFoundError(f"The file with key \"{file_key}\" doesn't exists")
            if r.json()['error']['message'] == "URL Not Found":
                raise _UrlNotFoundError()

        elif r.status_code == 503:
            raise _ServiceUnavailableError()

    def delete(self, file_key: str) -> None:
        r = _requests.post(
            url=_BASE_URL + '/files/delete',
            headers={'bot_token': self.BOT_TOKEN},
            data={
                'file_key': file_key
            }
        )
        if r.status_code == 200:
            return

        elif r.status_code == 400:
            raise _BadRequestError()

        elif r.status_code == 401:
            raise _UnauthorizedError()

        elif r.status_code == 404:
            if r.json()['error']['message'] == "File Not Found":
                raise FileNotFoundError(f"The file with key \"{file_key}\" doesn't exists")
            if r.json()['error']['message'] == "URL Not Found":
                raise _UrlNotFoundError()

        elif r.status_code == 503:
            raise _ServiceUnavailableError()
