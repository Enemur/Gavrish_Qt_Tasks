#ifndef UIELEMENTS_H
#define UIELEMENTS_H

#include "QTreeView"
#include "QMainWindow"
#include <QListView>
#include <QPlainTextEdit>
#include <QComboBox>
#include <QRadioButton>
#include <QCheckBox>

struct UiElements
{
    QMainWindow* window;

    QTreeView* dirView;
    QListView* filesView;
    QPlainTextEdit* textView;
    QComboBox* colors;

    QRadioButton* rbCp;
    QRadioButton* rbUTF8;

    QCheckBox* cbBold;
    QCheckBox* cbItalic;
    QCheckBox* cbUnderline;
};

#endif // UIELEMENTS_H
