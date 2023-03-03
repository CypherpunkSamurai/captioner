from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtWidgets import QPlainTextEdit
from src.completion import TagCompleter


class CompletedPlainText(QPlainTextEdit):
    """
    enchanted plain text edit

    """

    def __init__(self, *args):
        # init self
        super(CompletedPlainText, self).__init__(*args)

        # completer
        self.completer = TagCompleter("tags.txt")
        self.completer.setWidget(self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setMaxVisibleItems(10)
        # connect completer activation to the word completion function
        self.completer.activated.connect(self.completion)

    def getWordUnderCursor(self) -> str:
        """
        returns the word under the cursor

        note: needs to be called after super of the event or you will get word before the key is entered

        :return:
        """
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.WordUnderCursor)
        return cursor.selectedText()

    def completion(self, completion, *args, **kwargs):
        """
        completion

        :param completion:
        :return:
        """

        # cursor
        cursor = self.textCursor()

        # get the extra characters required to complete the word
        extra = len(completion) - len(self.completer.completionPrefix())

        # if the completion word is not rewriting the current word
        # i.e. we understand if there are characters remaining to be written
        # (completion word is of len > current word)
        if extra > 0:
            cursor.movePosition(cursor.Left)
            cursor.movePosition(cursor.EndOfWord)
            # add the remaining char for the word
            cursor.insertText(completion[-extra:])

        # rewrite the current word
        else:
            cursor.movePosition(cursor.StartOfWord)
            cursor.select(QtGui.QTextCursor.WordUnderCursor)
            cursor.removeSelectedText()
            cursor.insertText(completion)

        self.setTextCursor(cursor)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        """
        handles keypress events

        :param e:
        :return:
        """

        if self.completer is not None and self.completer.popup().isVisible():
            # The following keys are forwarded by the completer to the widget.
            if e.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                e.ignore()
                # Let the completer do default behavior.
                return

        # send the key event first
        super(CompletedPlainText, self).keyPressEvent(e)

        # continue and handle key press
        if e.text().isalnum():

            # get completion prefix
            completion_prefix = self.getWordUnderCursor()

            # check if completion prefix is updated
            if completion_prefix != self.completer.completionPrefix():
                # set completion prefix
                self.completer.setCompletionPrefix(completion_prefix)

                # popup
                self.completer.popup()
                self.completer.popup().setCurrentIndex(
                    self.completer.completionModel().index(0, 0)
                )

            # popup
            c = self.cursorRect()
            c.setWidth(self.completer.popup().sizeHintForColumn(
                0) + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(c)

        else:
            self.completer.popup().hide()
