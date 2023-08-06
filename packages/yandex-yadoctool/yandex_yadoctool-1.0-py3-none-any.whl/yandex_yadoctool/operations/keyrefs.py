#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from platform import system
import os
import re
import traceback 
  
class Keyrefs:
    def __init__(self):
        self.slasher = '\\' if system() == 'Windows' else '/'
        
        pre = 'INFO  '
        warn = 'WARNING  '

        all_keydefs = ''
        support_keydefs = []
        service_keydefs = []
        outsource_keydefs = []

        main_path = self.specify_main_path(os.getcwd())
        doc_name = main_path.split(self.slasher)[-1]
        file_name = doc_name+'-extrefs'
        main_path_to_show = main_path.split(f'{self.slasher}src2{self.slasher}')[1]

        print (f'{pre}Path to update: {main_path_to_show}')
        print (f'{pre}The process has started.\n')
        for path, _, files in os.walk(main_path):
            for file in files:      
                base, ext = os.path.splitext(file)
                if ext == '.ditamap' and not('.yoda' in path):
                    os.chdir(path)               
                    os.rename(file, base + '.xml')
                    file = base + '.xml' 
                    try:
                        with open(file, encoding='utf-8') as doc:
                            content = doc.read()
                            if ('<keydef' in content) and ('scope="external"' in content):
                                print(f'{pre}Found {base}.ditamap, adapting...')                        
                                keydef_begin = content.find('<keydef')
                                keydef_end = self.find_keydef_end(content, keydef_begin)                    
                                while keydef_begin!=-1:
                                    if ('scope="external"' in content[keydef_begin:keydef_end]) and (content[keydef_begin-4:keydef_begin]!='<!--'):
                                        keydef = content[keydef_begin:keydef_end]
                                        content = content.replace(keydef, f'<!--{keydef}-->')                                
                                        keys_begin = content.find('keys="', keydef_begin)+6
                                        keys_end = content.find('"', keys_begin)
                                        key_name = content[keys_begin:keys_end]
                                        main_href_begin = content.find('href="', keydef_begin)+6
                                        main_href_end = content.find('"', main_href_begin)
                                        main_href = content[main_href_begin:main_href_end].lstrip(' \n\t').rstrip(' /\n\t').replace('\n','').replace('\t','').replace('http://', 'https://')
                                        new_key_name, key_type = self.generate_key_name(main_href)
                                        full_new_keydef = self.old_keydef_to_new_keydef(keydef, new_key_name)
                                        keydef_begin = content.find('<keydef', keydef_end)                                
                                        keydef_end = self.find_keydef_end(content, keydef_begin)
                                        while f'keys="{key_name}"' in content[keydef_begin:keydef_end]:
                                            keydef = content[keydef_begin:keydef_end]
                                            content = content.replace(keydef, f'<!--{keydef}-->')                                    
                                            full_new_keydef = full_new_keydef + self.old_keydef_to_new_keydef(keydef, new_key_name)
                                            keydef_begin = content.find('<keydef', keydef_end)
                                            keydef_end = self.find_keydef_end(content, keydef_begin) 
                                        if not(self.keydef_is_exist(full_new_keydef, all_keydefs)):
                                            dub_is_exist = False
                                            if (f'keys="{new_key_name}"' in all_keydefs):
                                                changing_key_name, dub_is_exist = self.kill_duplicates(new_key_name, full_new_keydef, all_keydefs)
                                                full_new_keydef = full_new_keydef.replace(f'keys="{new_key_name}"', f'keys="{changing_key_name}"')
                                                new_key_name = changing_key_name      
                                            if dub_is_exist==False:
                                                all_keydefs = all_keydefs + '\n' + full_new_keydef
                                                if key_type == 'support':
                                                    support_keydefs.append(full_new_keydef)
                                                elif key_type == 'service':
                                                    service_keydefs.append(full_new_keydef)
                                                else:
                                                    outsource_keydefs.append(full_new_keydef)
                                                all_keydefs = all_keydefs + '\n' + full_new_keydef  
                                        if key_name != new_key_name:
                                            for path_1, _1, files_1 in os.walk(main_path):
                                                for file_1 in files_1:
                                                    base_1, ext_1 = os.path.splitext(file_1)
                                                    if ext_1=='.dita' and not('.yoda' in path_1):
                                                        os.chdir(path_1)
                                                        os.rename(file_1, base_1 + '.xml')
                                                        file_1 = base_1 + '.xml' 
                                                        with open(file_1, encoding='utf-8') as doc_1:   
                                                            content_1 = doc_1.read()
                                                            if f'keyref="{key_name}"' in content_1:
                                                                content_1 = content_1.replace(f'keyref="{key_name}"', f'keyref="{new_key_name}"')
                                                                with open(file_1, encoding='utf-8', mode='w') as doc_1:
                                                                    doc_1.write(content_1)
                                                        os.rename(file_1, base_1 + '.dita')
                                    else:
                                        keydef_begin = content.find('<keydef', keydef_end)
                                        keydef_end = content.find('/>', keydef_begin)
                                os.chdir(path)                                
                                with open(file, encoding='utf-8', mode='w') as doc:
                                    doc.write(content)
                                print(f'{pre}Imported {base}.ditamap to a new map.')                            
                    except Exception as exc:                
                        print(f'{warn} There is an error in {base}.ditamap. Skip it.')
                        print(f'...\n{traceback.format_exc()}...')
                        os.chdir(path)
                        with open(file, encoding='utf-8', mode='w') as doc:
                            doc.write(content)                
                        os.rename(file, base + '.ditamap')                
                        continue                                        
                    
                    os.chdir(path)
                    os.rename(file, base + '.ditamap')
                    
                    
                if ext == '.dita' and not('.yoda' in path):
                    os.chdir(path)               
                    os.rename(file, base + '.xml')
                    file = base + '.xml'                
                    try:            
                        with open(file, encoding='utf-8') as doc:
                            content = doc.read()
                            start_content = content
                            html_i = content.find('scope="external"')                    
                            while html_i!=-1:                      
                                left_xref_begin = content.rfind('<', 0, html_i)
                                if content[left_xref_begin:left_xref_begin+5]=='<xref':
                                    first_xref = left_xref_begin
                                    left_xref_end = content.find('>', html_i)
                                    a = content.find('/>', left_xref_begin)
                                    b = content.find('</xref>', left_xref_begin)
                                    if a!=-1 and (a < b or b==-1):
                                        right_xref = a
                                        xref_end = a+1
                                        text = '' 
                                    else: 
                                        right_xref = b 
                                        xref_end = b+6
                                        text = content[left_xref_end+1:right_xref].lstrip(' ').rstrip(' ').replace('\n','').replace('\t','')                            
                                    main_href_begin = content.find('href="', left_xref_begin)+6
                                    main_href_end = content.find('"', main_href_begin)
                                    main_href = content[main_href_begin:main_href_end].lstrip(' \n\t').rstrip(' /\n\t').replace('\n','').replace('\t','').replace(' ','')
                                    key_name, key_type = self.generate_key_name(main_href)
                                    text = content[left_xref_end+1:right_xref].lstrip(' ').rstrip(' ').replace('\n','').replace('\t','')
                                    full_xref = content[left_xref_begin:xref_end+1]
                                    full_keydef = self.href_to_keydef(full_xref, key_name)
                                    left_xref_begin = content.find('<xref', xref_end+1)
                                    while (left_xref_begin!=-1 and (content[xref_end+1:left_xref_begin].replace('\n','').replace('\t','').replace(' ','')=='')):
                                        last_xref_end = xref_end
                                        a = content.find('/>', left_xref_begin)
                                        b = content.find('</xref>', left_xref_begin)
                                        if a!=-1 and (a < b or b==-1): 
                                            xref_end = a+1
                                        else: 
                                            xref_end = b+6 
                                        xref = content[left_xref_begin:xref_end+1]
                                        if not('keyref="') in xref:
                                            full_xref = full_xref + xref                               
                                            full_keydef = full_keydef + self.href_to_keydef(xref, key_name)
                                            left_xref_begin = content.find('<xref', xref_end+1)
                                        else:
                                            left_xref_begin=-1
                                            xref_end = last_xref_end
                                    full_xref = content[first_xref:xref_end+1].rstrip(' \t\n')
                                    if not(self.keydef_is_exist(full_keydef, all_keydefs)):
                                        dub_is_exist=False
                                        if (f'keys="{key_name}"' in all_keydefs):
                                            new_key_name, dub_is_exist = self.kill_duplicates(key_name, full_keydef, all_keydefs)
                                            full_keydef = full_keydef.replace(f'keys="{key_name}"', f'keys="{new_key_name}"')
                                            key_name = new_key_name
                                        if dub_is_exist==False:
                                            all_keydefs = all_keydefs + '\n' + full_keydef
                                            if key_type == 'support':
                                                support_keydefs.append(full_keydef)
                                            elif key_type == 'service':
                                                service_keydefs.append(full_keydef)
                                            else:
                                                outsource_keydefs.append(full_keydef)
                                            all_keydefs = all_keydefs + '\n' + full_keydef
                                    if text == '':  
                                        key_xref = f'<xref keyref="{key_name}"/>'
                                    else: 
                                        key_xref = f'<xref keyref="{key_name}">{text}</xref>'                            
                                    content = content.replace(full_xref, key_xref)               
                                html_i = content.find('scope="external"', html_i+1)
                            if content != start_content:
                                with open(file, mode='w', encoding='utf-8') as doc:
                                    doc.write(content)                                                                      
                                
                    except Exception as exc:                
                        print(f'{warn}There is an error in {base}.dita. Skip it.')
                        print(f'...\n{traceback.format_exc()}...')
                        os.rename(file, base + '.dita')                
                        continue

                    os.rename(file, base + '.dita')

        os.chdir(main_path)
        with open(f'{file_name}.xml', mode='w', encoding='utf-8') as doc:
            support_keydefs = '\n'.join(sorted(support_keydefs))
            service_keydefs = '\n'.join(sorted(service_keydefs))
            outsource_keydefs = '\n'.join(sorted(outsource_keydefs))
            
            result = ("<?xml version='1.0' encoding='utf-8'?>\n"
                           f'<map xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsa8="http://dita.oasis-open.org/architecture/2005/" id="{file_name}" title="Карта внешних ссылок" xml:lang="ru" xsi:noNamespaceSchemaLocation="urn:yandex:names:tc:dita:xsd:yandexMap.xsd:1.3">\n'
                           '  <topicmeta>\n'
                           '    <prodinfo>\n'
                           '      <prodname> Карта внешних ссылок </prodname>\n'
                           '    </prodinfo>\n'
                           '  </topicmeta>\n\n'
                           '  <topichead>\n'
                           '    <topicmeta>\n'
                           '      <navtitle> Справка Яндекса </navtitle>\n'
                           '    </topicmeta>\n\n'
                           f'{support_keydefs}'                
                           '\n  </topichead>\n\n'
                           '  <topichead>\n'
                           '    <topicmeta>\n'                  
                           '      <navtitle> Сервисы Яндекса </navtitle>\n'
                           '    </topicmeta>\n\n'
                           f'{service_keydefs}'                   
                           '\n  </topichead>\n\n'
                           '  <topichead>\n'
                           '    <topicmeta>\n'
                           '      <navtitle> Сторонние ресурсы </navtitle>\n'
                           '    </topicmeta>\n\n'
                           f'{outsource_keydefs}'                   
                           '\n  </topichead>\n'
                           '\n'
                           '</map>')
            doc.write(result)
        if os.path.exists(f'{file_name}.ditamap'):
            os.remove(f'{file_name}.ditamap')    
        os.rename(f'{file_name}.xml', f'{file_name}.ditamap')

        doc_ditamap = f'{doc_name}-guide'
        if os.path.exists(f'{doc_ditamap}.ditamap'):
            os.rename(f'{doc_ditamap}.ditamap', f'{doc_ditamap}.xml')
            with open(f'{doc_ditamap}.xml', encoding='utf-8') as doc:
                content = doc.read()
                if not(f'<mapref href="{file_name}.ditamap"' in content):
                    ditamap_end = content.rfind('</map>')
                    content = content[:ditamap_end]+f'  <mapref href="{file_name}.ditamap" format="ditamap" processing-role="resource-only"/>\n'+content[ditamap_end:]
                    with open(f'{doc_ditamap}.xml', encoding='utf-8', mode='w') as doc:
                       doc.write(content)                
            os.rename(f'{doc_ditamap}.xml', f'{doc_ditamap}.ditamap')            
            
        print(f'\n{pre}Done! Check results.')
        print(f'{pre}Created {file_name}.ditamap in {main_path_to_show}.')

    def specify_main_path(self, main_path):
        src2 = main_path.rfind(f'{self.slasher}src2{self.slasher}')
        language = main_path.find(self.slasher, src2+6) 
        doc_name = main_path.find(self.slasher, language+5)
        end = main_path.find(self.slasher, doc_name)
        if end != -1:
            main_path = main_path[:end]
        return main_path
     
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
            name_type = 'support'
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
                name_type = 'support'
            elif ('yandex.' in href) and ('yandsearch?' in href or 'search/?' in href):
                key_name = 'yandex_search_query'
                name_type = 'service'       
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
                name_type = 'service'
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
                name_type = 'service'            
            else:
                key_name = self.turn_symbols_to_dash(key_name).replace('/','-')
                name_type = 'outsource'
                if len(key_name) > 55:
                    key_name = key_name[:56].rstrip('-')
            key_name = key_name.lower()        
            transl = {'ь': '', 'ъ': '', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'jo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shh', 'ы': 'y', 'э': 'je', 'ю': 'ju', 'я': 'ya'}
            alphabet = ['ь', 'ъ', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ы', 'э', 'ю', 'я']        
            if [i in alphabet for i in key_name]:
                for key in transl:
                    key_name = key_name.replace(key, transl[key])
                    
        return key_name, name_type

    def href_to_keydef(self, xref, key_name):
        href_begin = xref.find('href="')+6
        href_end = xref.find('"', href_begin)
        href = xref[href_begin:href_end].lstrip(' \n\t').rstrip(' \n\t').replace('\n','').replace('\t','').replace('http://', 'https://')
        if href[0]!='/' and href.count('/')>2:
            href = href.rstrip('/')
        if ('locale="' in xref):                     
            locale_begin = xref.find('locale="')+8
            locale_end = xref.find('"', locale_begin)
            locale = xref[locale_begin:locale_end].lstrip(' \n\t').rstrip(' /\n\t').replace('\n','').replace('\t','')
            keydef = f'    <keydef keys="{key_name}" locale="{locale}" href="{href}" scope="external" format="html"/>\n'
        else:
            keydef = f'    <keydef keys="{key_name}" href="{href}" scope="external" format="html"/>\n'
        return keydef
        
    def old_keydef_to_new_keydef(self, keydef, key_name):
        href_begin = keydef.find('href="')+6
        href_end = keydef.find('"', href_begin)
        href = keydef[href_begin:href_end].lstrip(' \n\t').rstrip(' \n\t').replace('\n','').replace('\t','').replace('http://', 'https://')
        if href[0]!='/' and href.count('/')>2:
            href = href.rstrip('/')
        if ('locale="' in keydef):                     
            locale_begin = keydef.find('locale="')+8
            locale_end = keydef.find('"', locale_begin)
            locale = keydef[locale_begin:locale_end].lstrip(' \n\t').rstrip(' /\n\t').replace('\n','').replace('\t','')
            new_keydef = f'    <keydef keys="{key_name}" locale="{locale}" href="{href}" scope="external" format="html"/>\n'
        else:
            new_keydef = f'    <keydef keys="{key_name}" href="{href}" scope="external" format="html"/>\n'
        return new_keydef    
        
    def keydef_is_exist(self, full_keydef, all_keydefs):
        keydefs = full_keydef.split('\n')
        keydefs.remove('')
        keydefs.sort()
        all_keydefs_array = all_keydefs.split('\n\n')
        for existing_full_keydef in all_keydefs_array:
            existing_keydefs = existing_full_keydef.split('\n')
            existing_keydefs.sort()
            if keydefs == existing_keydefs:
                return True
        return False
        
    def kill_duplicates(self, key_name, full_keydef, all_keydefs):
        dub_is_exist = False
        if 'search_query' in key_name:
            max_num = 100
        else:
            max_num = 20
        if (f'keys="{key_name}_01"' in all_keydefs):
            for i in range(max_num):
                if i<10:
                    istring = f'0{i}'
                else:
                    istring = i
                if self.keydef_is_exist(full_keydef.replace(f'keys="{key_name}"', f'keys="{key_name}_{istring}"'), all_keydefs):
                    new_key_name = f'{key_name}_{istring}'
                    dub_is_exist = True
                    break
                else:
                    if i<9:
                        istring = f'0{i+1}'
                    else:
                        istring = i+1               
                    if not (f'keys="{key_name}_{istring}"' in all_keydefs):
                        new_key_name = f'{key_name}_{istring}'
                        break
        else:        
            new_key_name = key_name + '_01'
        return (new_key_name, dub_is_exist)
        
    def find_keydef_end(self, content, begin):
        a = content.find('/>', begin)
        b = content.find('</keydef>', begin)
        if a!=-1 and (a < b or b==-1):
            keydef_end = a+2 
        else: 
            keydef_end = b+9
        return keydef_end