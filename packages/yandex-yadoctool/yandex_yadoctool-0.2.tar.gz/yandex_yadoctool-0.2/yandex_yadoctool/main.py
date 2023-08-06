#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

from yandex_yadoctool.operations.corrector import Corrector
from yandex_yadoctool.operations.locales import Locales
from yandex_yadoctool.operations.keyrefs import Keyrefs

def collect_args():
    parser = argparse.ArgumentParser(prog="yadoctool",
                                     description='Инструмент для оптимизации работы с DITA-документацией.',
                                     )
                                     
    subparsers = parser.add_subparsers(dest='command', title='subcommands', help='additional help')

    corrector = subparsers.add_parser('corrector', help="Скрипт для поиска опечаток и простейших ошибок в документации.")
    corrector.add_argument("-f", type=str, help="название файла. Например, --f auth.dita")

    locales = subparsers.add_parser('locales', help="Интерфейс для разметки ru-ссылок на другие dita-локали.")
    
    keyrefs = subparsers.add_parser('keyrefs', help="Скрипт для автозамены внешних ссылок на ключи.")
    
    return parser.parse_args()
    
def main():
    args = collect_args()
    
    if args.command == "corrector":
        Corrector('all' if args.f is None else args.f)
    elif args.command == "locales":
        Locales()
    elif args.command == "keyrefs":
        Keyrefs()
    else:
        print('Check help o.o')


if __name__ == '__main__':
    main()