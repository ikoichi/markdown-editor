'''
Created on 05/nov/2013

@author: <luca.restagno@gmail.com>
'''
import json, Constants

class Model():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.CURRENT_THEME = self.get_from_config("current_theme")
        self.load_css()

        self.RECENT_DOCUMENTS = self.get_recent_documents()

        self.FILE_PATH = ""
        self.TABS = [{ "path": "" }]
        self.ACTIVE_TAB = 0

    def get_file_name(self, file_path):
        path = str(file_path)
        t = path.split("/")
        return t[ len(t)-1 ]

    def get_file_folder(self, file_path):
        path = file_path
        t = path.split("/")
        str = ""
        for ix in range(len(t)-1):
            str = str + t[ix] + "/"

        return str

    def is_document_present(self, file_path):
        for ix in range(len(self.TABS)):
            if self.TABS[ ix ]['path'] == file_path:
                return ix
        return -1

    def append_document(self, file_path):
        self.TABS.append({ "path": file_path })
        self.ACTIVE_TAB = len(self.TABS)-1
        self.set_document_path(file_path)

    def set_active_tab(self, index):
        self.ACTIVE_TAB = index
        self.FILE_PATH = self.TABS[ index ]['path']

    def set_document_path(self, file_path):
        self.FILE_PATH = file_path

    def save_document_path(self, file_path):
        self.TABS[ self.ACTIVE_TAB ]['path'] = file_path

    def get_document_path(self):
        return self.FILE_PATH

    def load_css(self):
        self.THEMES = self.get_from_config("themes")
        for theme in self.THEMES:
            if int(theme["id"]) == int(self.CURRENT_THEME):
                self.base_css = self.get_file_content( theme["file"] )
                break

    def set_css(self, theme_index):
        self.CURRENT_THEME = theme_index
        self.load_css()
        self.save_in_config( "current_theme", int(self.CURRENT_THEME) )

    def get_css(self):
        return self.base_css

    def get_file_content(self, filename):
        try:
            f = open(filename, 'r')
            return f.read()
        except Exception:
            return False


    def write_file_content(self, filename, data):
        f = open(filename, 'w')
        f.write( str(data) )
        f.close()
        return True

    def get_recent_documents(self):
        result = self.get_file_content(Constants.CONFIG_FILE)
        data = json.loads(result)
        if "recent_documents" in data and type(data) is not None:
            return data["recent_documents"]
        else:
            return []

    def add_recent_document(self, path):
        if self.RECENT_DOCUMENTS is None:
            self.RECENT_DOCUMENTS = []
        l = len(self.RECENT_DOCUMENTS)
        t = self.RECENT_DOCUMENTS[:l]

        for ix in range(len(t)):
            if t[ ix ] == path:
                t.pop(ix)
                break

        self.RECENT_DOCUMENTS = []
        self.RECENT_DOCUMENTS.append( str(path) )
        self.RECENT_DOCUMENTS.extend(t)

        if len(self.RECENT_DOCUMENTS) > 11:
            self.RECENT_DOCUMENTS.pop()

        result = self.get_file_content( Constants.CONFIG_FILE )
        data = json.loads(result)
        data['recent_documents'] = self.RECENT_DOCUMENTS

        self.write_file_content(Constants.CONFIG_FILE, json.dumps(data))

    def remove_tab(self, index):
        self.TABS.pop(index)

    def get_browser_path(self):
        return self.get_from_config("browser")

    def get_browser_name(self):
        browser_path = self.get_from_config("browser")
        t = browser_path.split( "/" )
        return t[ len(t)-1 ]

    def get_from_config(self, key):
        result = self.get_file_content( Constants.CONFIG_FILE )
        data = json.loads(result)
        if key in data and type(data) is not None:
            return data[ key ]
        else:
            return None

    def save_in_config(self, key, value):
        result = self.get_file_content( Constants.CONFIG_FILE )
        data = json.loads(result)
        data[ key ] = value
        self.write_file_content(Constants.CONFIG_FILE, json.dumps(data))
        
