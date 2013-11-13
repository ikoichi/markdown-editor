'''
Created on 13/nov/2013

@author: <luca.restagno@gmail.com>
'''

from PyQt4 import QtGui
import Model, Controller, View
    
def main():
    
    app = QtGui.QApplication([])
    model = Model.Model()
    view = View.View()
    controller = Controller.Controller(view, model)
    app.exec_()

if __name__ == '__main__':
    main()