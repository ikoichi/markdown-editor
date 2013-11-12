'''
Created on 08/nov/2013

@author: <luca.restagno@gmail.com>
'''
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import Constants
class MarkdownHighlighter(QSyntaxHighlighter):
    '''
    classdocs
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        super(MarkdownHighlighter, self).__init__(parent)
        
        self.h1_color               = '#6C78C4'
        self.h2_color               = '#6C78C4'
        self.h3_color               = '#6C78C4'
        self.h4_color               = '#268BD2'
        self.h5_color               = '#268BD2'
        self.h6_color               = '#268BD2'
        self.bold_color             = '#DC322F'
        self.italic_color           = '#CB4B16'
        self.link_color             = '#4E27A6'
        self.code_color             = '#008C3F'
        self.anchor_color           = '#BF6211'
        self.block_quotes_color     = '#93A1A1'
        self.html_entity_color      = '#8871C4'

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.darkBlue)
        keywordFormat.setFontWeight(QFont.Bold)

        keywordPatterns = []

        self.highlightingRules = [(QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        # italic
        italicFormat = QTextCharFormat()
        italicFormat.setForeground(QColor(self.italic_color))
        italicFormat.setFontItalic(True)
        self.highlightingRules.append((QRegExp("\*.*\*"),italicFormat))
        
        # bold
        boldFormat = QTextCharFormat()
        boldFormat.setForeground(QColor(self.italic_color))
        boldFormat.setFontWeight(99)
        self.highlightingRules.append((QRegExp("\*\*.*\*\*"),boldFormat))
        
        # h1
        h1Format = QTextCharFormat()
        h1Format.setForeground(QColor(self.h1_color))
        h1Format.setFontWeight(99)
        h1Format.setFontPointSize(18)
        self.highlightingRules.append((QRegExp("^#.*$"),h1Format))
        
        # h2
        h2Format = QTextCharFormat()
        h2Format.setForeground(QColor(self.h2_color))
        h2Format.setFontWeight(99)
        h2Format.setFontPointSize(16)
        self.highlightingRules.append((QRegExp("^##.*$"),h2Format))
        
        # h3
        h3Format = QTextCharFormat()
        h3Format.setForeground(QColor(self.h3_color))
        h3Format.setFontWeight(99)
        h3Format.setFontPointSize(14)
        self.highlightingRules.append((QRegExp("^###.*$"),h3Format))
        
        # h4
        h4Format = QTextCharFormat()
        h4Format.setForeground(QColor(self.h4_color))
        h4Format.setFontWeight(99)
        h4Format.setFontPointSize(12)
        self.highlightingRules.append((QRegExp("^####.*$"),h4Format))
        
        # h5
        h5Format = QTextCharFormat()
        h5Format.setForeground(QColor(self.h5_color))
        h5Format.setFontWeight(99)
        h5Format.setFontPointSize(10)
        self.highlightingRules.append((QRegExp("^#####.*$"),h5Format))
        
        # h6
        h6Format = QTextCharFormat()
        h6Format.setForeground(QColor(self.h6_color))
        h6Format.setFontWeight(99)
        h6Format.setFontPointSize(10)
        self.highlightingRules.append((QRegExp("^######.*$"),h6Format))
        
        # link
        linkFormat = QTextCharFormat()
        linkFormat.setForeground(QColor(self.link_color))
        self.highlightingRules.append((QRegExp("<.*>"),linkFormat))
        
        # anchor
        anchorFormat = QTextCharFormat()
        anchorFormat.setForeground(QColor(self.anchor_color))
        self.highlightingRules.append((QRegExp("\[.*\]\(.*\)"),anchorFormat))
        
        #code
        codeFormat = QTextCharFormat()
        codeFormat.setForeground(QColor(self.code_color))
        codeFormat.setFontPointSize(10)
        codeFormat.setFontWeight(75)
        self.highlightingRules.append((QRegExp("`.*`"),codeFormat))
        
        codeFormat2 = QTextCharFormat()
        codeFormat2.setForeground(QColor(self.code_color))
        codeFormat2.setFontPointSize(10)
        codeFormat2.setFontWeight(75)
        self.highlightingRules.append((QRegExp("\t.*$"),codeFormat2))
        
        # block quotes
        blockQuotesFormat = QTextCharFormat()
        blockQuotesFormat.setForeground(QColor(self.block_quotes_color))
        self.highlightingRules.append((QRegExp("^> "),blockQuotesFormat))
        
        # html entity
        htmlEntityFormat = QTextCharFormat()
        htmlEntityFormat.setForeground(QColor(self.html_entity_color))
        self.highlightingRules.append((QRegExp("&.*;"),htmlEntityFormat))

#         functionFormat = QTextCharFormat()
#         functionFormat.setFontItalic(True)
#         functionFormat.setForeground(Qt.blue)
#         self.highlightingRules.append((QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),functionFormat))
#  
#         self.commentStartExpression = QRegExp("/\\*")
#         self.commentEndExpression = QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)
        