#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests
import re

class Corrector:
    def __init__(self, focus):
        self.main_path = self.specify_main_path(os.getcwd())
        self.main_path_to_show = self.main_path.split('\src2\\')[1]
        
        if focus != 'all':
            with open(focus, encoding='utf-8') as doc:
                path = os.getcwd()
                content = self.clean_content(doc.read())
                self.check_text(content, focus, path, True)
        else:
            print (f'Проверяем документ {self.main_path_to_show}...') 
            for path, _, files in os.walk(self.main_path):
                for file in files:
                    base, ext = os.path.splitext(file)
                    if ext == '.dita' and not('.yoda' in path):
                        os.chdir(path)
                        os.rename(file, base + '.xml')
                        file = base + '.xml'
                        with open(file, encoding='utf-8') as doc:
                            content = self.clean_content(doc.read())
                            self.check_text(content, file, path, False)
                        os.rename(file, base + '.dita')
        print('Готово!')  
            
    def specify_main_path(self, main_path):
        src2 = main_path.rfind('\src2\\')
        language = main_path.find('\\', src2+6) 
        doc_name = main_path.find('\\', language+5)
        end = main_path.find('\\', doc_name)
        if end != -1:
            main_path = main_path[:end]
        return main_path
       
    def clean_content(self, content):
        CLEANR = re.compile(r'<[^>]+>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        content_without_tags = re.sub(CLEANR, ' ', content)
        content_strings = content_without_tags.split('\n')
        cleaned_content = ''
        for string in content_strings:
            string = string.lstrip(' ').rstrip(' ')
            cleaned_content = cleaned_content + string + '\n'
        return cleaned_content
        
    def check_text(self, content, source, path, checking_one_file):
        file_path = self.main_path_to_show+path.split(self.main_path)[1]+'\\'+source.replace('.xml', '.dita')
        url = 'https://speller.yandex.net/services/spellservice.json/checkText'
        params = {
            "text": content,
            "lang": 'ru',
            "options": 12
        }
        response = requests.post(url, data=params)
        comments = response.json()
        for comment in comments:
            if comment["s"] == [comment["word"]]:
                comments.remove(comment)
        if comments == [] and checking_one_file:
            print(f'\nС {file_path} всё хорошо, замечаний нет')
        elif comments != []:
            print(f'\nВозможно, в {file_path} есть ошибки:')
            i=0
            for comment in comments:
                i+=1
                if comment["word"] in comment["s"]:
                    comment["s"].remove(comment["word"])
                print(f'{i}. «{comment["word"]}» (строка {comment["row"]+1}). Варианты: {"«"+("», «").join(comment["s"])+"»"}')
                
