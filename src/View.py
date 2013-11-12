'''
Created on 05/nov/2013

@author: restaglu
'''

import MarkdownHighlighter, Constants
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtWebKit import QWebView
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
from MarkdownEditor import Model
from MarkdownEditor import Controller

class myTextEdit(QtGui.QTextEdit):
        
    def wheelEvent(self, event):
        
        numDegrees = event.delta() / 8;
        numSteps = -( numDegrees / 15 );
        
        scrollbar = self.verticalScrollBar()
        step = scrollbar.pageStep() / 10
        
        document_h = self.document().size().height()
        
        preview = self.preview
        h = preview.page().mainFrame().contentsSize().height()
        
        ratio = h / document_h
        
        s = preview.page().mainFrame().scrollPosition().y()
        
        new_value = s + step * numSteps * ratio
        if new_value < 0:
            new_value = 0

        #preview.scroll( 0 , new_value )
        #preview.page().mainFrame().scroll(0, new_value )
        preview.page().mainFrame().setScrollPosition(QtCore.QPoint(0, new_value ))
        
        s = scrollbar.value()
        new_value = s + step * numSteps
        if new_value < 0:
            new_value = 0
        
        scrollbar.setValue( new_value )
        
        preview.reload()
        
        event.accept()
    

class View(QtGui.QMainWindow):
    
    def __init__(self):
        super(View, self).__init__()
        
        _widget = QtGui.QWidget()
        
        self.initUI(_widget)
        
    @pyqtSlot()
    def scroll(self):
        
        inputEdit = self.active_input()
        scrollbar = inputEdit.verticalScrollBar()
        scroll_pos = scrollbar.value()
        
        document_h = inputEdit.document().size().height()
        
        ratio = scroll_pos / document_h
        
        preview = self.active_preview()
        h = preview.page().mainFrame().contentsSize().height()
        
        preview.scroll( 0 , ratio * h )
        preview.page().mainFrame().scroll(0, ratio * h )
        preview.page().mainFrame().setScrollPosition(QtCore.QPoint(0, ratio * h ))
        
    def add_tab(self, title):
        tab = QtGui.QWidget()
        
        inputEdit = myTextEdit()
        MarkdownHighlighter.MarkdownHighlighter( inputEdit )
        font = QtGui.QFont();
        font.setFamily( Constants.EDIT_FONT );
        font.setStyleHint(QtGui.QFont.Monospace);
        font.setFixedPitch(True);
        font.setPointSize(10);
        inputEdit.setFont( font )
        inputEdit.setTabStopWidth(20)
        
        inputEdit.setGeometry(0,0,200,200)
        preview = QWebView()
        preview.setGeometry(0,200,200,200)
        inputEdit.preview = preview
        
        scrollbar = inputEdit.verticalScrollBar()
        scrollbar.connect(scrollbar,SIGNAL("valueChanged()"),self,SLOT("scroll()"))
        scrollbar.connect(scrollbar,SIGNAL("rangeChanged()"),self,SLOT("scroll()"))
        scrollbar.connect(scrollbar,SIGNAL("sliderPressed()"),self,SLOT("scroll()"))
        scrollbar.connect(scrollbar,SIGNAL("sliderMoved()"),self,SLOT("scroll()"))
        scrollbar.connect(scrollbar,SIGNAL("sliderReleased()"),self,SLOT("scroll()"))
        scrollbar.connect(scrollbar,SIGNAL("actionTriggered()"),self,SLOT("scroll()"))
        
        self.tabs.addTab(tab,title)
        #self.tabs.setWindowTitle('PyQt QTabWidget Add Tabs and Widgets Inside Tab')
        
        tab_hbox = QtGui.QHBoxLayout()
        
        tab_hbox.addWidget(inputEdit)
        tab_hbox.addWidget(preview)
        tab.setLayout(tab_hbox)
        
        return [inputEdit, preview]
    
    def remove_tab(self, index):
        self.tabs.removeTab(index)
        
    def initUI(self, widget):
        
        hbox = QtGui.QHBoxLayout()
        
        self.tabs = QtGui.QTabWidget()
        self.tabs.setTabsClosable(True)
        
        hbox.addWidget(self.tabs)
        widget.setLayout(hbox)
        
        self.setCentralWidget(widget)
        
        self.makeMenubar() 
        
        self.update_status('Ready')
        
        self.resize(800, 600)
        self.showMaximized()
        #self.showFullScreen()
        self.center()
        self.setWindowTitle( Constants.APP_TITLE )
        self.setWindowIcon(QtGui.QIcon('images/applications-internet.png'))  
    
        self.show()
        
        # Preferences Panel
        self.prefs = QtGui.QWidget()
        self.prefs.resize(500, 150)
        self.prefs.setWindowTitle('Preferences')
        
        formLayout = QtGui.QFormLayout()
        self.browserLineEdit = QtGui.QLineEdit()
        self.browserLineEdit.setReadOnly(True)
        
        self.browserButton = QtGui.QPushButton("&Select")
        
        rowLayout = QtGui.QHBoxLayout()
        
        rowLayout.addWidget(QtGui.QLabel("Preview browser"))
        rowLayout.addWidget(self.browserLineEdit)
        rowLayout.addWidget(self.browserButton)
        
        formLayout.addRow(rowLayout)
        
        self.prefs.setLayout(formLayout)
        
    def update_status(self, status):
        self.statusBar().showMessage( status )
        
    def makeMenubar(self):
        
        self.newAction = QtGui.QAction(QtGui.QIcon('images/document-new.png'), '&New', self)
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.setStatusTip('New (Ctrl+N)')
        
        self.openAction = QtGui.QAction(QtGui.QIcon('images/document-open.png'), '&Open', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Open file (Ctrl+O)')
        
        self.saveAction = QtGui.QAction(QtGui.QIcon('images/document-save.png'), '&Save', self)
        self.saveAction.setDisabled(True)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save (Ctrl+S)')
        
        self.exportHTMLAction = QtGui.QAction(QtGui.QIcon('images/export-html.gif'), '&Export to HTML', self)
        self.exportHTMLAction.setDisabled(True)
        self.exportHTMLAction.setShortcut('Ctrl+H')
        self.exportHTMLAction.setStatusTip('Export to HTML (Ctrl+H)')
        
        self.viewInBrowserAction = QtGui.QAction(QtGui.QIcon('images/internet-web-browser.png'), '&Browser preview', self)
        self.viewInBrowserAction.setDisabled(True)
        self.viewInBrowserAction.setShortcut('Ctrl+P')
        self.viewInBrowserAction.setStatusTip('Browser preview (Ctrl+P)')
        
        self.exitAction = QtGui.QAction(QtGui.QIcon('images/application-exit.png'), '&Exit', self)        
        self.exitAction.setShortcut('Alt+F4')
        self.exitAction.setStatusTip('Exit application (Alt+F4)')
        self.exitAction.triggered.connect(QtGui.qApp.quit)
        
        self.boldAction = QtGui.QAction(QtGui.QIcon('images/format-text-bold.png'), '&Bold', self)        
        self.boldAction.setShortcut('Ctrl+B')
        self.boldAction.setStatusTip('Bold (Ctrl+B)')
        self.boldAction.triggered.connect(self.text_make_bold)
        
        self.italicAction = QtGui.QAction(QtGui.QIcon('images/format-text-italic.png'), '&Italic', self)        
        self.italicAction.setShortcut('Ctrl+I')
        self.italicAction.setStatusTip('Italic (Ctrl+I)')
        self.italicAction.triggered.connect(self.text_make_italic)
        
        self.quoteAction = QtGui.QAction(QtGui.QIcon('images/quote-left.png'), '&Quote', self)        
        self.quoteAction.setShortcut('Ctrl+Q')
        self.quoteAction.setStatusTip('Quotes (Ctrl+Q)')
        self.quoteAction.triggered.connect(self.text_make_quote)
        
        self.codeAction = QtGui.QAction(QtGui.QIcon('images/code.png'), '&Code', self)        
        self.codeAction.setShortcut('Ctrl+K')
        self.codeAction.setStatusTip('Code (Ctrl+K)')
        self.codeAction.triggered.connect(self.text_make_code)
        
        self.toolbar = self.addToolBar('File actions')
        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)
        
        self.toolbar2 = self.addToolBar('Editor actions')
        
        self.toolbar2.addAction(self.boldAction)
        self.toolbar2.addAction(self.italicAction)
        self.toolbar2.addAction(self.quoteAction)
        self.toolbar2.addAction(self.codeAction)
        
        self.toolbar3 = self.addToolBar('Export actions')
        
        self.toolbar3.addAction(self.exportHTMLAction)
        self.toolbar3.addAction(self.viewInBrowserAction)
        
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        
        fileMenu.addAction(self.exitAction)
        
        self.mapper = QtCore.QSignalMapper(self)
        self.recentDocumentMenu = QtGui.QMenu('&Recent documents', self)
        self.recentDocumentMenu.setDisabled(True)
        
        fileMenu.insertMenu(self.exitAction, self.recentDocumentMenu)
        
        fileMenu.insertSeparator(self.exitAction)
        
        actionsMenu = menubar.addMenu('&Actions')
        actionsMenu.addAction(self.boldAction)
        actionsMenu.addAction(self.italicAction)
        actionsMenu.addAction(self.quoteAction)
        actionsMenu.addAction(self.codeAction)
        actionsMenu.insertSeparator(self.exportHTMLAction)
        actionsMenu.addAction(self.exportHTMLAction)
        actionsMenu.addAction(self.viewInBrowserAction)
        
        toolsMenu = menubar.addMenu('&Tools')
        
        self.themesMapper = QtCore.QSignalMapper(self)
        self.themesMenu = QtGui.QMenu('&Themes', self)
        
        self.preferencesAction = QtGui.QAction(QtGui.QIcon('images/system-run.png'), '&Preferences', self)        
        self.preferencesAction.setShortcut('F7')
        self.preferencesAction.setStatusTip('Preferences')
        
        self.syntaxAction = QtGui.QAction(QtGui.QIcon(), '&Syntax reference', self)
        self.syntaxAction.setStatusTip('Syntax reference')
        
        self.aboutAction = QtGui.QAction(QtGui.QIcon(''), '&About', self)        
        self.aboutAction.setStatusTip('About')
        self.aboutAction.triggered.connect(self.dialog_about)
        
        toolsMenu.addAction(self.preferencesAction)
        toolsMenu.addAction(self.syntaxAction)
        toolsMenu.addAction(self.aboutAction)
        toolsMenu.insertMenu(self.preferencesAction, self.themesMenu)
        
    def show_preferences(self):
        self.prefs.show()
        
    def text_make_quote(self):
        inputEdit = self.active_input()
        cursor = inputEdit.textCursor()
        textSelected = cursor.selectedText()
        cursor.insertText( "\n> "+textSelected )
    
    def text_make_bold(self):
        self.format_text( "**" )
        
    def text_make_italic(self):
        self.format_text( "*" )
        
    def text_make_code(self):
        self.format_text( "`" )
            
    def format_text(self, character):
        inputEdit = self.active_input()
        cursor = inputEdit.textCursor()
        textSelected = cursor.selectedText()
        cursor.insertText( character + textSelected + character )
        if len(textSelected) == 0:
            cursor.setPosition( cursor.position() - len(character) )
            inputEdit.setTextCursor(cursor)
        
    def add_recent_document(self, file_path):
        recentFileAction = QtGui.QAction('&'+str(file_path), self)
        self.mapper.setMapping(recentFileAction, str(file_path))
        self.recentDocumentMenu.addAction(recentFileAction)
        return recentFileAction
    
    def add_theme_menu_item(self, name, theme_index):
        themeAction = QtGui.QAction('&'+str(name), self)
        self.themesMapper.setMapping(themeAction, str(theme_index))
        self.themesMenu.addAction(themeAction)
        return themeAction
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def set_document(self, document):
        inputEdit = self.active_input()
        inputEdit.setText( QtCore.QString(document) )
        
    def get_current_document_content(self):
        inputEdit = self.active_input()
        return unicode(inputEdit.toPlainText())
        
    def select_file(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Select file', "*.md", "Markdown .md")
        print( "Selected file: " + fname )
        if fname:
            return fname
        else:
            return False
        
    def save_file_picker(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file', "*.md", "Markdown .md")
        print( "Selected file: " + fname )
        if fname:
            return fname
        else:
            return False
        
    def select_browser(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Select browser', "*.exe", "Executable")
        if fname:
            return fname
        else:
            return False

    def active_input(self):
        return self.tabs.currentWidget().findChildren(QtGui.QTextEdit)[0]
    
    def active_preview(self):
        return self.tabs.currentWidget().findChildren(QWebView)[0]
    
    def change_active_tab(self, index):
        self.tabs.setCurrentIndex(index)
        
    def no_file_alert(self):
        QtGui.QMessageBox.warning(self, "Alert", "The file does not exist")
        
    def dialog_about(self):
        QtGui.QMessageBox.about(self, "About", "Markdown Editor version "+Constants.VERSION+"<br>Author: "+Constants.AUTHOR)

def main():
    
    app = QtGui.QApplication([])
    model = Model.Model()
    view = View()
    controller = Controller.Controller(view, model)
    app.exec_()

if __name__ == '__main__':
    main()