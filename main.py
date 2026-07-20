#from apps.telegram_bot.telegram_bot.main import main

def main():
    if(args.train):
        import training.train as train
        # Ща будет жесткий дриллинг аргументов
        from shared.config import DATA_RAW_FILE
        print(f"Запущено в режиме тренировки, указанный путь к тренировочным данным: {args.file or DATA_RAW_FILE}")
        train.main(args)

    elif(args.bot):
        import apps.telegram_bot.telegram_bot.main as bot
        print("Запуск сервиса с телеграм ботом")
        bot.main()

    elif(args.worker):
        import apps.ml_worker.ml_worker.worker as worker
        print("Запуск сервиса для разметки сообщений")
        worker.main()

    elif(args.api):
        import apps.api.api.app as api
        print("Запуск сервиса с API")
        api.main() 

    else:
        print("Пожалуйста, укажите запускаемый сервис:\n\n-t --train  -  тренировка моделей\n-f --file   -  путь к разметке для тренировки\n-a --api    -  апи для работы с фронтендом\n-w --worker -  запуск сервиса разметки сообщений\n-b --bot    -  сервис чтения сообщений из телеграм")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file")
    parser.add_argument("-t", "--train", action="store_true")
    parser.add_argument("-b", "--bot", action="store_true")
    parser.add_argument("-w", "--worker", action="store_true")
    parser.add_argument("-a", "--api", action="store_true")
    args = parser.parse_args()
    main()