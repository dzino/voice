#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from subprocess import call
from re import sub
from argparse import ArgumentParser


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
        :var  festival: программа синтезирования голоса
        :type festival: str
        """

        try:
            print('Проверка наличия программы')
            call(['festival','-v'])
            call('clear')
        except OSError as e:
            print('NO  "festival", начало установки')
            call('sudo apt-get install festival festvox-ru', shell=True)
            call('clear')

    def cycle_input(self):

        """
        :param  cycle           : цикл интерфейса
        :type   cycle           : bool
        :param  text            : пользовательский текст для озвучки
        :type   text            : text
        :method cyrillic_filter : фильтрация латинских символов
        :method to_voice        : синтез голоса
        """

        cycle = True
        while cycle:
            self.text = input('Озвучить: ')
            self.cyrillic_filter()
            self.to_voice()

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
    obj.cycle_input()