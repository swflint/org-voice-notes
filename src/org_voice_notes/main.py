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

import os
import os.path as osp
import glob

from datetime import datetime
from tqdm import tqdm
from queue import Queue

from argparse import ArgumentParser

from .transcription import Transcription

def main():
    parser = ArgumentParser(description='A tool to convert voice notes to an Org file.')

    parser.add_argument('--output', '-o',
                        help = 'output file',
                        dest='output',
                        required = True)

    parser.add_argument('--api-key', '-k',
                        help = 'the assemblyai api key to use',
                        dest = 'key')

    parser.add_argument('--directory', '-d',
                        help = 'the directory tree containing audio files',
                        dest = 'directory',
                        required = True)

    parser.add_argument('--delete', '-D',
                        help = 'delete transcription and audio file',
                        dest = 'delete',
                        default = False,
                        action = 'store_true')

    args = parser.parse_args()

    if args.key == None:
        if os.environ.get('ASSEMBLY_AI_KEY'):
            args.key = os.environ.get('ASSEMBLY_AI_KEY')
        else:
            parser.error("An API key must be provided as an argument or in the ASSEMBLY_AI_KEY environment variable.")

    if osp.exists(args.output):
        output_file = open(args.output, 'a')
    else:
        output_file = open(args.output, 'w')
    
    transcriptions = []
    for file_name in tqdm(glob.iglob(f'{args.directory}/**/*.mp3')):
        transcriptions.append(Transcription(args.key, file_name))

    with tqdm(total = len(transcriptions), desc = 'Transcriptions remaining') as progress:
        while len(transcriptions) != 0:
            transcription = transcriptions.pop(0)
            return_val = transcription.get_transcription()
            if return_val == None:
                transcriptions.append(transcription)
            else:
                file_path = transcription.file_path
                (base, file_name) = osp.split(file_path)
                (base, folder) = osp.split(base)
                ts = datetime.strptime(file_name, "%y%m%d_%H%M.mp3")
                output_file.write(f"\n* <{ts.strftime('%Y-%m-%d %a %H:%M')}> {folder}\n\n{return_val}\n")
                if args.delete:
                    transcription.delete_recording()
                    transcription.delete_transcription()
                progress.update(1)

    output_file.close()

    
