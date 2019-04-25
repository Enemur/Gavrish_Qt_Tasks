#include "appmodel.h"

void AppModel::readFile() const
{
    QFile file(_currentFilePath);

    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
        throw std::runtime_error("Error opennig file");

    QTextStream stream(&file);
    stream.setCodec(_codec.toStdString().c_str());

    const quint64 maxlen = 16;
    QString str;n
    while(!stream.atEnd())
         str.append(stream.read(maxlen));

    emit fileTextChanged(str);
}

void AppModel::writeFile(const QString &fileaPth, QString fileText) const
{
    QFile file(filePath);
    if(!file.open(QIODevice::WriteOnly | QIODevice::Truncate)){
        throw std::runtime_error("Error opening file");
    }

    QTextStream out(&file);
    out.setCodec(_codec.toStdString().c_str());

    QTextStream in(&fileText);
    const quint64 maxlen = 16;

    while(!in.atEnd()) {
        out << in.read(maxlen);

    if (in.status() != QTextStream::Ok)
        throw std::runtime_error("Error reading text");

    if (out.status() != QTextStream::Ok)
        throw std::runtime_error("Error writing file");
    }
}

AppModel::AppModel()
    :_colors()
{
    _colors.append(Qt::black);
    _colors.append(Qt::yellow);
    _colors.append(Qt::red);
    _colors.append(Qt::blue);
    _colors.append(Qt::green);
}

void AppModel::setDirectoryPath(const QString directoryPath)
{
    _curentDirectoryPath = directoryPath;
}

void AppModel::setFilePath(const QString &filePath)
{
    _currentFilePath = filePath;
}

void AppModel::setCodec(const QString &codec)
{
    _codec = codec;
}

QString AppModel::getDirectoryPath() const
{
    return _curentDirectoryPath;
}

QString AppModel::getFilePath() const
{
    return _currentFilePath;
}

QString AppModel::getCodec() const
{
    return _codec;
}

Qt::GlobalColor AppModel::getColor(int index) const
{
    if (index < 0 || index > _colors.size())
        throw std::runtime_error("Unknown color");

    return _colors[index];
}

AppModel::~AppModel()
{

}
