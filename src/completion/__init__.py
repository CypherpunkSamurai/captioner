import os
import logging
from PyQt5 import QtWidgets
from PyQt5.QtCore import QStringListModel, Qt
from .engines import FastAutocompleteEngine


class TagCompleter(QtWidgets.QCompleter):
    """
    Custom QCompleter
    """

    def __init__(self, wordlist_file: str, *args, **kwargs):
        # super class init
        super(TagCompleter, self).__init__(*args, **kwargs)

        # custom model
        self.model = QStringListModel()
        # set model
        self.setModel(self.model)

        # load tags
        self.tag_list_path = str(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), wordlist_file)
        )
        self.engine = FastAutocompleteEngine(self.tag_list_path)

        # set completer settings
        self.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)

    def _update_model(self, completion_prefix):
        """
        internal function to update completion prefix before providing completions

        :param completion_prefix:
        :return:
        """

        # check
        if completion_prefix and self.engine.is_working:
            self.model.setStringList(
                self.engine.complete(completion_prefix)
            )
            logging.info(f"completions: {self.model.stringList()}")
        else:
            self.model.setStringList([])

    def splitPath(self, text):

        # log
        logging.info(f"completing: {text}")

        # update self model
        self._update_model(text)

        # call super to return completions
        return super().splitPath(text)
