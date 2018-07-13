#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from subprocess import call
from re import sub
from argparse import ArgumentParser
from imp import find_module


class voice:

    def __init__(self):

        self.text = ""
        self.parameters()

    def parameters(self):

        """ установка параметров в файле """

        parser = ArgumentParser()
        parser.add_argument("-s", "--speed", help="Регулировка скорости воспроизведения. Целое число. Запускать с правами администратора. Пример: 25000")
        args = parser.parse_args()
        if args.speed:
            self.replace_line_in_file('/etc/festival.scm', 'Audio_Command "aplay',
                '(Parameter.set \'Audio_Command "aplay -q -c 1 -t raw -f s16 -r %s $FILE")\n' % args.speed)

    @staticmethod
    def replace_line_in_file(file_name, source_text, replace_text):

        """
        изменение строки в файле
        :param source_text : отрывок текста из строки для поиска в файле
        :type  source_text : str
        :param replace_text: заменяющая строка
        :type  replace_text: str
        """

        word = source_text
        inp = open(file_name).readlines()
        for i in iter(inp):
            if word in i:
                source_text = i

        fileObj = open(file_name, 'r')
        text = fileObj.read()
        fileObj.close()

        fileObj = open(file_name, 'w')
        fileObj.write(text.replace(source_text, replace_text))
        fileObj.close()

    @staticmethod
    def install_utility():

        """
        проверка наличия программы - нет, устанавливаем
        :var  keyboard: глобал. горяч. клавиши
        :type keyboard: str
        :var  tkinter : получение данных из буфера обмена
        :type tkinter : str
        :var  festival: программа синтезирования голоса
        :type festival: str
        """

        try:
            print('Проверка программы "keyboard"')
            find_module('keyboard')
            call('clear')
        except:
            print('NO  "keyboard", начало установки')
            call('sudo python3 -m pip install keyboard', shell=True)
            call('clear')

        try:
            print('Проверка программы "tkinter"')
            find_module('tkinter')
            call('clear')
        except:
            print('NO  "tkinter", начало установки')
            call('sudo apt-get install python3-tk', shell=True)
            call('clear')

        try:
            print('Проверка программы "festival"')
            call(['festival','-v'])
            call('clear')
        except OSError as e:
            print('NO  "festival", начало установки')
            call('sudo apt-get install festival festvox-ru', shell=True)
            call('clear')

    def hot_key(self):

        """
        прослушивание горячих клавиш
        """

        print('Горячие клавиши: ctrl+c')
        add_hotkey('ctrl+c', self.cycle_input)
        wait()

    def cycle_input(self):

        """
        Цикл
        :param  text           : текст из буфера обмена
        :type   text           : text
        :method cyrillic_filter: фильтрация латинских символов
        :method to_voice       : синтез голоса
        """

        self.text = self.getClipboardData()
        self.cyrillic_filter()
        if isinstance(self.text, str):
            print(self.text)
            self.to_voice()
        else:
            print('Не строка')

    @staticmethod
    def getClipboardData():

        """
        получение данных из буфера обмена
        """

        c = Tk()
        c.withdraw()
        clip = c.clipboard_get()
        c.update()
        c.destroy()
        return clip

    def cyrillic_filter(self):

        """
        удаляем символы латыни из строки и тире (при переносах в книгах)
        :return text: отфильтрованное значение, введенное пользователем
        :type   text: text
        """

        self.text = sub(r'[^а-яёА-ЯЁ0-9\s]', '', self.text)
        self.text = sub("^\s+|\n|\r|\s+$", '', self.text)

    def to_voice(self):

        """ озвучивание """

        #call('clear')
        print('Чтение...')
        if self.text: call(['echo "%s" | festival --tts --language russian'%self.text], shell=True)
        #call('clear')


if __name__ == '__main__':
    obj = voice()
    obj.install_utility()
    from keyboard import add_hotkey, wait
    from tkinter import Tk
    obj.hot_key()