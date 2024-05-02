from os.path import exists
import logging

from HitoriGameLogic import HitoriBoardChecker, HitoriBoard
from Load_and_Print import HitoriLoader, HitoriPrint

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.DEBUG)


def main():
    logging.info("Начало работы программы")

    # Проверяем, существует ли сохраненная доска
    if exists('board.pkl'):
        # Загружаем доску
        logging.info("Загружена старая доска")
        board = HitoriLoader.load()
        print("Дорешиваем старую доску...")

    else:
        HitoriPrint.print_instruction(1)
        lengths = input()
        logging.debug(f"Длина и ширина доски: {lengths}")

        if lengths == '--help':
            HitoriPrint.help()
            return

        try:
            # Проверяем, являются ли введенные значения числами
            int(lengths.split()[0])
            int(lengths.split()[1])
        except Exception:
            HitoriPrint.lengths_is_not_number()
            logging.debug(HitoriPrint.lengths_is_not_number())
            return

        length = lengths.split()

        HitoriPrint.print_instruction(2)
        input_board = input()
        logging.debug(f"Доска: {input_board}")

        board_digits = input_board.split()

        if len(board_digits) != int(length[0]) * int(length[1]):
            HitoriPrint.not_all_numbers()
            return

        HitoriPrint.print_instruction(3)
        number_components = input()
        logging.debug(f"количество компонент: {number_components}")

        try:
            # Проверяем, является ли введенное значение числом
            num_comp = int(number_components)
        except Exception:
            HitoriPrint.wrong_number_components()
            logging.debug(HitoriPrint.wrong_number_components())
            return

        if num_comp <= 0:
            HitoriPrint.wrong_number_components()
            return
        board = HitoriBoard(int(length[0]), int(length[1]), board_digits, HitoriBoardChecker(num_comp))



    # Решаем головоломку
    board.solve()

    # Удаляем сохраненную доску
    HitoriLoader.remove()

    # Выводим результат
    HitoriPrint.print_result(board)
    logging.debug(f"Готовая доска: {board}")
    logging.info("Работа программы завершена")


if __name__ == "__main__":
    main()