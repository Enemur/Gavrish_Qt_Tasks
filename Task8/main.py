import IDrive
from YandexDrive import YandexDrive


def main():
    try:
        yandex_drive: IDrive = YandexDrive()
        file = yandex_drive.download_file('https://yadi.sk/i/0UkjTnFSeBaiYw')

        print("Куда сохранить: ", end='')
        save_file_path = input()

        with open(save_file_path, 'wb') as outFile:
            outFile.write(file)
        print(f'Файл сохранен сюда: {save_file_path}')
    except Exception as error:
        print(str(error))


if __name__ == '__main__':
    main()
