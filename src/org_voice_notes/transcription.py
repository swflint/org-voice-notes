#!/usr/bin/env python
# coding: utf-8

# This file is a part of `org-voice-notes`.
#
# Copyright (c) 2021, Samuel W. Flint <swflint@flintfam.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import requests

class Transcription:
    def __init__(self, api_key, file_path):
        self.api_key = api_key
        self.file_path = file_path
        self.status = 'UNUPLOADED'
        self.upload_url = None
        self.request_id = None
        self.text = None
        self.paragraphs = None

    def __read_file(self, chunk_size=5242880):
        with open(self.file_path, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    def upload_file(self):
        if not self.upload_url:
            headers = {'authorization': self.api_key}
            response = requests.post('https://api.assemblyai.com/v2/upload',
                                     headers = headers,
                                     data = self.__read_file())
            data = response.json()
            self.upload_url = data['upload_url']
        return self.upload_url

    def get_transcription(self):
        if self.status == 'UNUPLOADED':
            self.upload_file()
            response = requests.post('https://api.assemblyai.com/v2/transcript',
                                     json = {'audio_url': self.upload_url},
                                     headers = {'authorization': self.api_key,
                                                'content-type': 'application/json'})
            data = response.json()
            self.status = data['status']
            self.request_id = data['id']
            return None
        if self.status != 'completed':
            response = requests.get(f'https://api.assemblyai.com/v2/transcript/{self.request_id}',
                                    headers = {'authorization': self.api_key,
                                               'content-type': 'application/json'})
            data = response.json()
            self.status = data['status']
            if self.status == 'completed':
                self.text = data['text']
        if self.status == 'completed':
            return self.text
        else:
            return None

    def get_paragraphs(self):
        transcription_status = self.get_transcription()
        if transcription_status != None:
            if self.paragraphs:
                return self.paragraphs
            else:
                response = requests.get(f'https://api.assemblyai.com/v2/transcript/{self.request_id}/paragraphs',
                                        headers = {'authorization': self.api_key,
                                               'content-type': 'application/json'})
                data = response.json()
                self.paragraphs = list(map(x: x['text'], data['paragraphs']))
                return self.paragraphs
        else:
            return None

    def delete_transcription(self):
        requests.delete(f'https://api.assemblyai.com/v2/transcript/{self.request_id}',
                        headers = {'authorization': self.api_key})
        return True

    def delete_recording(self):
        try:
            os.remove(self.file_path)
            return True
        except:
            return False
