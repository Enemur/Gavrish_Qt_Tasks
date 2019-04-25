#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "presenter.h"

#include <QMessageBox>
#include <QMainWindow>
#include "uielements.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
private:
    Ui::MainWindow *ui;

    Presenter* _presenter;
private:
    void setConnections();
    void about();
public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();
};

#endif // MAINWINDOW_H
