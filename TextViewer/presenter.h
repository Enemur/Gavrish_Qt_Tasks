#ifndef PRESENTER_H
#define PRESENTER_H

#include "appmodel.h"
#include "qobject.h"

#include <QFileDialog>
#include <QFileSystemModel>
#include <QListWidget>
#include <QTextEdit>
#include <QTreeView>
#include "uielements.h"
#include <QMessageBox>

class Presenter : public QObject
{
    Q_OBJECT
private:
    AppModel* _model;

    UiElements _uiElements;

    QFileSystemModel _dirModel;
    QFileSystemModel _fileModel;
private:
    void setConnections();

    void initDirView();
    void initFileView();
    void initColors();

    void error(const QString& message) const;

    void openDirectory(const QString directoryPath);
public:
    Presenter(UiElements uiElements);

    void setCodec(const QString& codec);

    ~Presenter();
public slots:
    void onDirViewDoubleClick(const QModelIndex &index);
    void onFileViewDoubleClick(const QModelIndex &index);
    void onOpenDirectoryClick();
    void onFileTextChanched(const QString fileText);
    void onSaveAsClick();

    void onSetBold(int state);
    void onSetItalic(int state);
    void onSetUnderline(int state);

    void onSetColor(int colorIndex);

    void reset();
};

#endif // PRESENTER_H
