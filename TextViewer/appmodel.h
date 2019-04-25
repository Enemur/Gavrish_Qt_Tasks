#ifndef APPMODEL_H
#define APPMODEL_H

#include "qobject.h"
#include "QFile"
#include "QTextStream"
#include "QList"

class AppModel : public QObject
{
    Q_OBJECT
private:
    QString _curentDirectoryPath;
    QString _currentFilePath;
    QString _codec;

    QList<Qt::GlobalColor> _colors;
private:
public:
    AppModel();

    void readFile() const;
    void writeFile(const QString& filePath, QString fileText) const;

    void setDirectoryPath(const QString directoryPath);
    void setFilePath(const QString& filePath);
    void setCodec(const QString& codec);

    QString getDirectoryPath() const;
    QString getFilePath() const;
    QString getCodec() const;
    Qt::GlobalColor getColor(int index)const;

    ~AppModel();
signals:
    void fileTextChanged(const QString& fileText) const;
};

#endif // APPMODEL_H
