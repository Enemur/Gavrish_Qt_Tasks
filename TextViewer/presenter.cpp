#include "presenter.h"

Presenter::Presenter(UiElements uiElements)
    :_model(new AppModel()),
     _uiElements(uiElements),
     _dirModel(),
     _fileModel()
{
    initDirView();
    initFileView();
    initColors();

    _model->setCodec(_uiElements.rbCp->text());

    setConnections();
}

void Presenter::setConnections()
{
    connect(_model, &AppModel::fileTextChanged, this, &Presenter::onFileTextChanched);
}

void Presenter::initDirView()
{
    _dirModel.setFilter(QDir::Dirs | QDir::Drives | QDir::NoDotAndDotDot | QDir::AllDirs);
    _dirModel.setRootPath("");
    _uiElements.dirView->setModel(&_dirModel);
    _uiElements.dirView->setRootIndex(_dirModel.index(""));
}

void Presenter::initFileView()
{
    _fileModel.setFilter(QDir::Files);
    _fileModel.setRootPath("");
    _uiElements.filesView->setModel(&_fileModel);
    _uiElements.filesView->setRootIndex(_fileModel.index(""));
}

void Presenter::initColors()
{
    _uiElements.colors->clear();

    _uiElements.colors->addItem("Black");
    _uiElements.colors->addItem("Yellow");
    _uiElements.colors->addItem("Red");
    _uiElements.colors->addItem("Blue");
    _uiElements.colors->addItem("Green");

    _uiElements.colors->setCurrentIndex(0);
}

void Presenter::error(const QString& message) const
{
    QMessageBox box;
    box.setWindowTitle("Error");
    box.setText(message);
    box.exec();
}

void Presenter::openDirectory(const QString directoryPath)
{
    _model->setDirectoryPath(directoryPath);

    _dirModel.setRootPath(directoryPath);
    _uiElements.dirView->setModel(&_dirModel);
    _uiElements.dirView->setRootIndex(_dirModel.index(directoryPath));

    _fileModel.setRootPath(directoryPath);
    _uiElements.filesView->setModel(&_fileModel);
    _uiElements.filesView->setRootIndex(_fileModel.index(directoryPath));

     _uiElements.textView->clear();
}

void Presenter::onDirViewDoubleClick(const QModelIndex &index)
{
    auto path = _dirModel.filePath(index);

    _fileModel.setRootPath(path);
    _uiElements.filesView->setModel(&_fileModel);
    _uiElements.filesView->setRootIndex(_fileModel.index(path));

     _uiElements.textView->clear();
}

void Presenter::onFileViewDoubleClick(const QModelIndex &index)
{
    auto path = _fileModel.filePath(index);
    QRegExp rg("*.txt");
    rg.setPatternSyntax(QRegExp::Wildcard);

    try
    {
        if (rg.exactMatch(path))
        {
            _model->setFilePath(path);
            _model->readFile();
        }
        else
        {
            _model->setFilePath("");
            _uiElements.textView->clear();
        }
    }
    catch(std::exception& e)
    {
        error(e.what());
    }
}

void Presenter::reset()
{
    try
    {
        _uiElements.rbCp->setChecked(true);
        _model->setCodec(_uiElements.rbCp->text());

        if (_model->getFilePath() != "")
            _model->readFile();

        _uiElements.colors->setCurrentIndex(0);

        _uiElements.cbBold->setCheckState(Qt::CheckState::Unchecked);
        _uiElements.cbItalic->setCheckState(Qt::CheckState::Unchecked);
        _uiElements.cbUnderline->setCheckState(Qt::CheckState::Unchecked);
    }
    catch(std::exception& e)
    {
        error(e.what());
    }
}

void Presenter::setCodec(const QString &codec)
{
    try
    {
        _model->setCodec(codec);
        _model->readFile();
    }
    catch(std::exception& e)
    {
        error(e.what());
    }
}

void Presenter::onFileTextChanched(const QString fileText)
{
    _uiElements.textView->clear();
    _uiElements.textView->insertPlainText(fileText);
}

void Presenter::onSaveAsClick()
{
    if (_model->getFilePath() != "")
    {
        try
        {
            auto filePath = QFileDialog::getSaveFileName(_uiElements.window, tr("Save File"), "", "*.txt");
            if (filePath == "")
                return;

            _model->writeFile(filePath, _uiElements.textView->toPlainText());
        }
        catch(std::exception& e)
        {
            error(e.what());
        }
    }
}

void Presenter::onSetBold(int state)
{
    auto font = QFont(_uiElements.textView->font());
    font.setBold(state);
    _uiElements.textView->setFont(font);
}

void Presenter::onSetItalic(int state)
{
    auto font = QFont(_uiElements.textView->font());
    font.setItalic(state);
    _uiElements.textView->setFont(font);
}

void Presenter::onSetUnderline(int state)
{
    auto font = QFont(_uiElements.textView->font());
    font.setUnderline(state);
    _uiElements.textView->setFont(font);
}

void Presenter::onSetColor(int colorIndex)
{
    auto p = _uiElements.textView->palette();
    auto color = _model->getColor(colorIndex);

    p.setColor(QPalette::Active, QPalette::Text, color);
    _uiElements.textView->setPalette(p);
    _uiElements.textView->setBackgroundVisible(false);
}

void Presenter::onOpenDirectoryClick()
{
    auto path = QFileDialog::getExistingDirectory(_uiElements.window,
                                                  tr("Open directory"),
                                                  "",
                                                  QFileDialog::ShowDirsOnly | QFileDialog::DontResolveSymlinks);
    openDirectory(path);
}

Presenter::~Presenter()
{
    delete _model;
}
