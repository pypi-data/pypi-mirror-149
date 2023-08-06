##
# File: LexerErrorListner.py
# Date: 11-Feb-2022
#
# Updates:
""" Inheritance of ANTLR ErrorListener for Lexer.
    @author: Masashi Yokochi
"""
import os

from antlr4.error.ErrorListener import ErrorListener


MAX_ERROR_REPORT = 1


class LexerErrorListener(ErrorListener):

    __messageList = None

    __filePath = None
    __fileName = None

    def __init__(self, filePath, fileName=None):

        self.__filePath = filePath

        self.__fileName = fileName\
            if fileName is not None and len(fileName) > 0\
            else os.path.basename(filePath)

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        if self.__messageList is None:
            self.__messageList = []

        if len(self.__messageList) >= MAX_ERROR_REPORT:
            return

        _msg = msg.split("'")
        length = 1 if 'alternative' in msg or len(_msg) < 2 else len(_msg[1])

        _dict = {'file_path': self.__filePath,
                 'file_name': self.__fileName,
                 'line_number': line,
                 'column_position': column,
                 'message': msg,
                 'marker': " " * (column) + "^" * (length)}

        _line = 1
        with open(self.__filePath, 'r', encoding='utf-8') as ifp:
            for content in ifp:
                if _line == line:
                    _dict['input'] = content.replace('\t', ' ')\
                        .replace('\r', ' ').replace('\n', ' ')\
                        .rstrip(' ')
                    break
                _line += 1

        if 'error at' in _dict['message']:  # lexer error
            try:
                p = _dict['message'].index('error at')
                _dict['message'] = _dict['message'][0:p] + 'error at:'
            except ValueError:
                pass

        self.__messageList.append(_dict)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        pass

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        pass

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        pass

    def getMessageList(self):
        return self.__messageList
