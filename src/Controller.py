'''
Created on 05/nov/2013

@author: <luca.restagno@gmail.com>
'''
import markdown, Constants
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot,SIGNAL
from subprocess import call

class Controller():
    '''
    classdocs
    '''

    def __init__(self, view, model):
        '''
        Constructor
        '''
        self.VIEW = view
        self.MODEL = model
        self.CONTROLLER = self
        
        self.VIEW.newAction.triggered.connect(self.new_file)
        self.VIEW.openAction.triggered.connect(self.open_file)
        self.VIEW.saveAction.triggered.connect(self.save_file)
        self.VIEW.exportHTMLAction.triggered.connect(self.export_html)
        self.VIEW.viewInBrowserAction.triggered.connect(self.preview_in_browser)
        self.VIEW.showInFolderAction.triggered.connect(self.open_folder)
        self.VIEW.preferencesAction.triggered.connect(self.show_preferences)
        self.VIEW.syntaxAction.triggered.connect(self.open_references)
        self.VIEW.browserButton.clicked.connect(self.select_browser)
        
        uis = self.VIEW.add_tab( Constants.EMPTY_TAB_TITLE )
        inputEdit = uis[0]
        inputEdit.connect(inputEdit,SIGNAL("textChanged()"),self.renderInput)
        #inputEdit.css = self.MODEL.get_css()
        
        self.VIEW.tabs.connect(self.VIEW.tabs,SIGNAL("currentChanged(int)"),self.tabChangedSlot)
        self.VIEW.tabs.connect(self.VIEW.tabs,SIGNAL("tabCloseRequested(int)"),self.tabCloseRequestedSlot)
        
        self.VIEW.mapper.mapped['QString'].connect(self.open_file_path)
        
        self.VIEW.themesMapper.mapped['QString'].connect(self.change_theme)
        
        self.refresh_recent_documents()
        self.load_themes()
        
    @pyqtSlot()
    def renderInput(self):
        
        html = markdown.markdown( unicode(self.VIEW.active_input().toPlainText() ) )
        self.VIEW.saveAction.setDisabled(False)
        
        preview = self.VIEW.active_preview() 
        y = preview.page().mainFrame().scrollPosition().y()
        data =QtCore.QString("<style>")
        data.append(QtCore.QString(self.MODEL.base_css))
        data.append("</style>")
        data.append(QtCore.QString(html))
        #data = QtCore.QByteArray("<style>"+ +"</style>" + html)
        preview.setContent( data.toUtf8() )
        
        preview.scroll(0, y)
        preview.page().mainFrame().scroll(0, y)
        preview.page().mainFrame().setScrollPosition(QtCore.QPoint(0, y))
        
        y = preview.page().mainFrame().scrollPosition().y()
        
        #preview.reload()
        
    @pyqtSlot(int)
    def tabChangedSlot(self,argTabIndex):
        self.MODEL.set_active_tab(argTabIndex)
        if self.MODEL.FILE_PATH == "":
            self.VIEW.exportHTMLAction.setDisabled(True)
            self.VIEW.viewInBrowserAction.setDisabled(True)
            self.VIEW.showInFolderAction.setDisabled(True)
        else:
            self.VIEW.exportHTMLAction.setDisabled(False)
            self.VIEW.viewInBrowserAction.setDisabled(False)
            self.VIEW.showInFolderAction.setDisabled(False)
        
        
    @pyqtSlot(int)
    def tabCloseRequestedSlot(self,argTabIndex):
        self.MODEL.remove_tab(argTabIndex)
        self.VIEW.remove_tab(argTabIndex)
        
    def show_preferences(self):
        self.VIEW.show_preferences()
        browser_name = self.MODEL.get_browser_name()
        self.VIEW.browserLineEdit.setText(browser_name)
        
    def open_folder(self):
        self.VIEW.open_folder(self.MODEL.get_file_folder( self.MODEL.FILE_PATH ))
        
    def select_browser(self):
        self.VIEW.prefs.close()
        browser_path = self.VIEW.select_browser()
        if browser_path is not None and browser_path != "" and browser_path is not False:
            self.MODEL.save_in_config("browser", str(browser_path))
            browser_name = self.MODEL.get_browser_name()
            self.VIEW.browserLineEdit.setText(browser_name)
            self.VIEW.prefs.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.VIEW.prefs.show()
        else:
            self.VIEW.prefs.show()
        
    def change_theme(self, theme_index):
        self.MODEL.set_css(theme_index)
        self.renderInput()
        
    def load_themes(self):
        for theme in self.MODEL.THEMES:
            action = self.VIEW.add_theme_menu_item( theme["name"], theme["id"] )
            action.triggered.connect(self.VIEW.themesMapper.map)
                
    def refresh_recent_documents(self):
        if len(self.MODEL.RECENT_DOCUMENTS) > 0:
            self.VIEW.recentDocumentMenu.setDisabled(False)
            self.VIEW.recentDocumentMenu.clear()
            for item in self.MODEL.RECENT_DOCUMENTS:
                action = self.VIEW.add_recent_document(str(item))
                action.triggered.connect(self.VIEW.mapper.map)
                
    def new_file(self):
        self.MODEL.append_document("")
        
        uis = self.VIEW.add_tab( Constants.EMPTY_TAB_TITLE )
        inputEdit = uis[0]
        inputEdit.connect(inputEdit,SIGNAL("textChanged()"),self.renderInput)
        inputEdit.css = self.MODEL.get_css()
        
        self.VIEW.change_active_tab( self.MODEL.ACTIVE_TAB )
    
    def open_file_path(self, file_path):
        file_content = self.MODEL.get_file_content(file_path)
        
        if file_content is False:
            self.VIEW.no_file_alert()
            return False
        
        doc_ix = self.MODEL.is_document_present(file_path)
        if doc_ix != -1:
            self.MODEL.ACTIVE_TAB = doc_ix
            self.MODEL.add_recent_document(file_path)
            self.VIEW.change_active_tab( self.MODEL.ACTIVE_TAB )
        else:
            self.MODEL.append_document(file_path)
            self.MODEL.add_recent_document(file_path)
            
            uis = self.VIEW.add_tab( self.MODEL.get_file_name(file_path) )
            inputEdit = uis[0]
            inputEdit.connect(inputEdit,SIGNAL("textChanged()"),self.renderInput)
            inputEdit.css = self.MODEL.get_css()
            
            self.VIEW.change_active_tab( self.MODEL.ACTIVE_TAB )
            self.VIEW.set_document(file_content)
            self.VIEW.saveAction.setDisabled(False)
            self.VIEW.exportHTMLAction.setDisabled(False)
            self.VIEW.viewInBrowserAction.setDisabled(False)
            self.VIEW.showInFolderAction.setDisabled(False)
        
        self.refresh_recent_documents()
        
        return file_path
        
    def open_file(self):
        file_path = self.VIEW.select_file()
        if file_path != False:
            self.open_file_path(file_path)
            
    
    def save_file(self):
        current_document = self.VIEW.get_current_document_content()
        if self.MODEL.FILE_PATH == '':
            file_path = self.VIEW.save_file_picker()
            if file_path != False:
                self.MODEL.FILE_PATH = file_path
                self.MODEL.save_document_path(file_path)
                self.MODEL.write_file_content( self.MODEL.FILE_PATH, current_document )
                self.MODEL.add_recent_document(file_path)
                
                self.VIEW.update_status('Document saved to ' + self.MODEL.FILE_PATH)
                self.VIEW.exportHTMLAction.setDisabled(False)
                self.VIEW.viewInBrowserAction.setDisabled(False)
                self.VIEW.showInFolderAction.setDisabled(False)
                self.VIEW.tabs.setTabText( self.MODEL.ACTIVE_TAB, self.MODEL.get_file_name( file_path ) ) 
                
                self.refresh_recent_documents()
                
        else:
            self.MODEL.write_file_content( self.MODEL.FILE_PATH, current_document )
            self.VIEW.update_status('Document saved to ' + self.MODEL.FILE_PATH)
        
    def export_html(self):
        export_path = self.MODEL.FILE_PATH.replace(".md", ".html")
        current_document = self.VIEW.get_current_document_content()
        
        html_document = "<!doctype html><html><body>"
        html_document += "<style type=\"text/css\">" + self.MODEL.base_css + "</style>"
        html_document += markdown.markdown( current_document )
        html_document += "</body></html>"
        
        result = self.MODEL.write_file_content(export_path, html_document)
        if result == True:
            self.VIEW.update_status('File exported to ' + export_path)
            return export_path
        else:
            self.VIEW.update_status('An error occurred...')
            return None
        
    def preview_in_browser(self):
        browser_path = self.MODEL.get_browser_path()
        if browser_path == "":
            self.select_browser()
        else:
            path = self.export_html()
            path = str(path).replace(":/", ":\\\\").replace("/", "\\")
            call([str(browser_path), path])
            
    def open_references(self):
        self.open_file_path( Constants.HELP_FILE )

        
        