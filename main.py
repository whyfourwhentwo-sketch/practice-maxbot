"""Запускает ТГ-бота"""

from apps.telegram_bot.telegram_bot.main import main
from training.train import train_main


from shared.config import DATA_FILE

if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file")
    parser.add_argument("-t", "--train", action="store_true")
    args = parser.parse_args()

    if(args.train):
        # Ща будет жесткий дриллинг аргументов
        print(f"Запущено в режиме тренировки, указанный путь к тренировочным данным: {args.file or DATA_FILE}")
        train_main(args)
    else:
        print("Запуск бота")
        main()
