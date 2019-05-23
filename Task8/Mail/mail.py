

# загрузку файла сделать и все
from Mail.cloud_mail import PyMailCloud
from Mail.consts import email, password

if __name__ == '__main__':
    print('started')
    a = PyMailCloud(email, password)
    f = a.get_folder_contents('')
    print(f)

    # result = a.upload_files('/', '/home/pavel/out.txt')
    # print(result)
    # a.download_file('/test.txt', '/home/pavel/downloadFile')
