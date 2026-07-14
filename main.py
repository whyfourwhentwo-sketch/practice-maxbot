"""Запускает ТГ-бота"""

from apps.telegram_bot.telegram_bot.main import main
from training.train import train_main
import apps.telegram_bot.telegram_bot.main as bot
import apps.ml_worker.ml_worker.worker as worker
import apps.api.api.app as api
from shared.config import DATA_FILE

if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file")
    parser.add_argument("-t", "--train", action="store_true")
    parser.add_argument("-b", "--bot", action="store_true")
    parser.add_argument("-w", "--worker", action="store_true")
    parser.add_argument("-a", "--api", action="store_true")
    args = parser.parse_args()

    if(args.train):
        # Ща будет жесткий дриллинг аргументов
        print(f"Запущено в режиме тренировки, указанный путь к тренировочным данным: {args.file or DATA_FILE}")
        train_main(args)
    if(args.bot):
        bot.main()
    if(args.worker):
        worker.main()
    if(args.api):
        api.main() 
    else:
        print("Запуск бота")
        main()
