#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import Tk, Label, Button, Checkbutton, Entry, Text, StringVar, BooleanVar, END
import re

class Locales:
    def __init__(self):
        self.root = Tk()
        self.root.title("Яндекс.Техпис: Генератор ссылок и ключей")
        self.root.geometry("550x420")
        self.root.resizable(width=False, height=False)

        self.href = StringVar()
        href_label = Label(text="Ссылка на .ru-домене")
        href_label.grid(row=3, padx=40, columnspan=11)
        href_entry = Entry(textvariable=self.href, width=78, justify='center')
        href_entry.grid(row=4, columnspan=11)

        self.xref_name = StringVar()
        xref_name_label = Label(text="Текст, под которым будет ссылка")
        xref_name_label.grid(row=5, padx=40, columnspan=11)
        xref_name_entry = Entry(textvariable=self.xref_name, width=78, justify='center')
        xref_name_entry.grid(row=6, padx=40, columnspan=11)

        self.key = BooleanVar()
        key_check = Checkbutton(text='Мне нужно сгенерировать ключи (keydef & keyref)', variable=self.key, command=self.keys_check)
        key_check.grid(row=10, columnspan=11)

        self.kz = BooleanVar(value=1)
        self.uz = BooleanVar(value=1)
        self.com = BooleanVar(value=1)
        self.tr = BooleanVar(value=1)
        self.ua = BooleanVar(value=1)
        self.by = BooleanVar()
        self.il = BooleanVar()
        kz_check = Checkbutton(text='kz', variable=self.kz)
        kz_check.grid(row=11,column=2)
        uz_check = Checkbutton(text='uz', variable=self.uz)
        uz_check.grid(row=11,column=3)
        com_check = Checkbutton(text='com', variable=self.com)
        com_check.grid(row=11,column=4)
        tr_check = Checkbutton(text='tr', variable=self.tr)
        tr_check.grid(row=11,column=5)
        ua_check = Checkbutton(text='ua', variable=self.ua)
        ua_check.grid(row=11,column=6)
        by_check = Checkbutton(text='by', variable=self.by)
        by_check.grid(row=11,column=7) 
        il_check = Checkbutton(text='il', variable=self.il)
        il_check.grid(row=11,column=8)
         
        result_button = Button(text="Разметить локали", command=self.display_result, bg='white', width=60)
        result_button.grid(row=14, columnspan=11, pady=5)

        self.result_text = Text(width=60, height=7)
        self.result_text.grid(row=15, columnspan=11)
        self.clipboard_button = Button(text="Копировать результат", command=self.clipboard, bg='white', width=30)
        self.clipboard_button.grid(row=16, columnspan=11, pady=5)

        self.key_result_text = Text(width=60, height=1)
        self.key_result_text.grid_remove()
        self.key_clipboard_button = Button(text="Копировать для .dita", command=self.key_clipboard, bg='white', width=30)
        self.key_clipboard_button.grid_remove()

        self.root.mainloop()

    def display_result(self):

        default_ru = self.href.get().rstrip('/').lstrip(' ')
        text = self.xref_name.get().lstrip(' ')
        if self.key.get()==1:
            keyname = self.generate_key_name(default_ru)
            ru = f'<keydef keys="{keyname}" href="{default_ru}" scope="external" format="html" locale="ru"/>'
            self.key_result_text.delete(1.0, END)
            self.key_result_text.insert(1.0, f'<xref keyref="{keyname}">{text}</xref>')        
        else:
            ru = f'<xref href="{default_ru}" scope="external" format="html" locale="ru">{text}</xref>'
        result=ru
        
        if self.kz.get()==1:
            result=result+ru.replace('.ru', '.kz').replace('locale="ru"', 'locale="kz"')
        if self.uz.get()==1:
            result=result+ru.replace('.ru', '.uz').replace('locale="ru"', 'locale="uz"')
        if self.ua.get()==1:
            result=result+ru.replace('.ru', '.ua').replace('locale="ru"', 'locale="ua"')
        if self.com.get()==1:
            result=result+ru.replace('.ru', '.com').replace('locale="ru"', 'locale="com"')
        if self.tr.get()==1:
            result=result+ru.replace('.ru', '.com.tr').replace('locale="ru"', 'locale="tr"')
        if self.by.get()==1:
            result=result+ru.replace('.ru', '.by').replace('locale="ru"', 'locale="by"')
        if self.il.get()==1:
            result=result+ru.replace('.ru', '.co.il').replace('locale="ru"', 'locale="il"')

        self.result_text.delete(1.0, END)
        self.result_text.insert(1.0, result)

    def keys_check(self):
        if self.key.get()==1:
            self.key_result_text.grid(row=17, columnspan=11)
            self.key_clipboard_button.grid(row=18, pady=5, columnspan=11)
            self.clipboard_button['text']='Копировать для .ditamap'
        else:
            self.key_result_text.grid_remove()
            self.key_clipboard_button.grid_remove()
            self.clipboard_button['text']='Копировать результат'
            
    def clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.result_text.get(1.0, END))

    def key_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.key_result_text.get(1.0, END))

    def turn_symbols_to_dash(self, string):
        for bad_symbol in self.bad_symbols:
            string = string.replace(bad_symbol,'-')
        string = re.sub('\-+','-', string).lstrip('-').rstrip('-') 
        return string  
            
    def format_service_and_alias(self, service, alias):
        service = self.turn_symbols_to_dash(service)       
        alias = self.turn_symbols_to_dash(alias)
        return(service, alias)
        
    def generate_key_name(self, href):
        self.bad_symbols = ['!', '#', '№', '$', '*', '~', '`', '_', '.', '&', '+', ',', ':', ';',
    '=', '?', '@', '<', '>', '[', ']', '{', '}', '|', '\\', '«', '»', '%', '%', '"', '\'', '/']
        key_name = href.rstrip(''.join(self.bad_symbols))
        domains = ['.ru', '.com', '.org', '.net', '.net.ru', '.com.ru', '.ua', '.by', '.eu', '.ee', '.lt', '.lv', '.md', '.uz',
                  '.mx', '.do', '.tm', '.de', '.ie', '.in', '.qa', '.so', '.nu', '.tj', '.dk', '.es', '.pt', '.pl', '.lu',
                  '.it', '.az', '.ro', '.rs', '.sk', '.no', '.asia', '.mobi', '.co.il', '.com.tr', '.kz']
        for domain in domains:
            if domain in key_name:
                if key_name.endswith(domain):
                    key_name = key_name[:key_name.rfind(domain)]
                else:
                    key_name = key_name.replace(f'{domain}/', '/', 1)
        key_name = key_name.replace('https://', '').replace('http://', '').replace('www.', '', 1).replace('.html','')
        if len(key_name)-6>0 and key_name[len(key_name)-6:len(key_name)]=='/index':
            key_name = key_name[:len(key_name)-6]
        if '../' in key_name:
            key_name_arr = key_name.split('../')
            key_name = '/' + key_name_arr[len(key_name_arr)-1]
        if 'support/plus' in key_name:
            plus_begin = key_name.find('/plus')
            plus_end = key_name.find('/', plus_begin+1)
            if plus_end == -1:
                key_name = key_name[:plus_begin+5]
            else:
                key_name = key_name.replace(key_name[plus_begin:plus_end], '/plus')      
        if key_name[0]=='/':
            href_array = key_name.replace('.html','').lstrip('/').rstrip('/').split('/')
            service = href_array[0]
            alias = href_array[len(href_array)-1]
            service, alias = self.format_service_and_alias(service, alias)
            if service==alias:
                key_name = f'yandexsupport_{service}'
            else:
                key_name = f'yandexsupport_{service}_{alias}'
        else:
            if ('yandex.' in href) and ('/support/' in href):
                href_array = key_name.split('/')
                if ('download.cdn' in href):
                    service = 'download'
                else:
                    service = href_array[2]
                alias = href_array[len(href_array)-1]
                service, alias = self.format_service_and_alias(service, alias)
                if service==alias:
                    key_name = f'yandexsupport_{service}'
                else:
                    key_name = f'yandexsupport_{service}_{alias}'
                if service == 'support':
                    key_name = key_name.replace('_support','')                
                name_type = 'support'
            elif ('yandex.' in href) and ('/dev/' in href):
                href_array = key_name.split('/')
                service = href_array[2]
                alias = href_array[len(href_array)-1]
                service, alias = self.format_service_and_alias(service, alias)     
                if service==alias:
                    key_name = f'yandexdev_{service}'
                else:
                    key_name = f'yandexdev_{service}_{alias}'
                if service == 'dev':
                    key_name = key_name.replace('_dev','')                
            elif ('yandex.' in href) and ('yandsearch?' in href or 'search/?' in href):
                key_name = 'yandex_search_query'       
            elif ('.yandex.' in href) and not('google.com' in href) and not('apple.com' in href):
                href_array_slash = key_name.split('/')
                href_array_dots = key_name.split('.')
                service = href_array_dots[0]
                alias = href_array_slash[len(href_array_slash)-1].replace('.yandex','')
                service, alias = self.format_service_and_alias(service, alias)       
                if service==alias:
                    key_name = f'yandex_{service}'   
                else:
                    key_name = f'yandex_{service}_{alias}'
            elif ('yandex.' in href) and not('google.com' in href) and not('apple.com' in href):
                href_array = key_name.split('/')
                if len(href_array)==1:
                    service = href_array[0]
                else:
                    service = href_array[1]
                alias = href_array[len(href_array)-1]
                service, alias = self.format_service_and_alias(service, alias)   
                if service==alias:
                    key_name = f'yandex_{service}'
                else:
                    key_name = f'yandex_{service}_{alias}'
                if service == 'yandex':
                    key_name = key_name.replace('_yandex','')            
            else:
                key_name = self.turn_symbols_to_dash(key_name).replace('/','-')
                if len(key_name) > 55:
                    key_name = key_name[:56].rstrip('-')
            key_name = key_name.lower()        
            transl = {'ь': '', 'ъ': '', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'jo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shh', 'ы': 'y', 'э': 'je', 'ю': 'ju', 'я': 'ya'}
            alphabet = ['ь', 'ъ', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'э', 'ю', 'я']        
            if [i in alphabet for i in key_name]:
                for key in transl:
                    key_name = key_name.replace(key, transl[key])
                    
        return key_name 