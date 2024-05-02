import logging
import pickle
from os import remove
from os.path import exists


class HitoriPrint:
    @staticmethod
    def help():
        print("Hitori Solver")
        print('Правила игры Хитори просты:')
        print('Необходимо закрасить некоторые ячейки таблицы, выполнив следующие условия:')
        print('- В любой строке/столбце ни одно число не должно повторяться.')
        print('- 2 чёрных ячейки не могут быть расположены рядом по горизонтали или вертикали.')
        print('- Все незакрашенные ячейки должны быть объединены в одну группу.')
        print()
        print('Для решения вашей головоломки введите число-ширину головоломок, затем нажмите Enter')
        print('и в одну строчку, через пробел введите числа из головоломки, например: 1 2 3 4')
        print('"+" в решении означает белую клеточку, а "-" черную')
        print("Нажмите любую клавишу, чтобы выйти..")
        input()

    @staticmethod
    def lengths_is_not_number():
        print('Ширина и высота должны быть целыми числами')


    @staticmethod
    def not_all_numbers():
        print("Количество цифр не соответствует ширине доски")

    @staticmethod
    def wrong_number_components():
        print("Неверный ввод. Число компонент связности должно быть натуральным числом")

    @staticmethod
    def print_result(board):
        if board.unsolvable:
            print("Ваша доска не имеет решения")
        else:
            if board.undetermined:
                print("Ваша доска не имеет единственного решения!")
                print("Вот лучшее, что мы смогли сделать:")
            else:
                print('Ваша доска:')
            print(board)
        print("Нажмите любую клавишу, чтобы выйти....")
        input()

    @staticmethod
    def print_add_rule_diogonal():
        print("Хотите добавить правило что все диогонали различны? Введите да или yes если это так")

    @staticmethod
    def print_instruction(number):
        instructions = {
            1: 'Введите высоту и ширину вашей доски через пробел или --help для получения дополнительной информации',
            2: 'Введите элементы доски в одну строку через пробел',
            3: 'Введите максимальное дозволенное число компонент связности'
        }

        if number in instructions:
            print(instructions[number])
        else:
            print('Неверный номер инструкции')


class HitoriLoader:
    @staticmethod
    def load():
        with open('board.pkl', 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def remove():
        if exists('board.pkl'):
            remove('board.pkl')

    @staticmethod
    def save(board):
        with open('board.pkl', 'wb') as f:
            pickle.dump(board, f)
# Статические методы используются в данном коде, так как они не требуют доступа к состоянию объекта класса и могут
# быть вызваны без создания экземпляра класса. В данном случае они используются для вывода информационных сообщений и
# ввода данных от пользователя. Такой подход позволяет логически объединить связанный функционал в одном классе и
# упростить его использование.