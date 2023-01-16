# @author: CypherpunkSamurai
# @license: MIT
# A program to assist in tagging of images


import sys
import shelve # for settings
from PyQt5 import QtWidgets, uic

# Required
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox

# Image
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QRectF


# Lists
from src import utils
import os


# theme
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import qApp


# Use MainWindow UI
from src.ui.MainWindow import Ui_MainWindow
from src.ui.Theme import ThemeChooseDlg



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
        Main Window Class
    """
    current_folder = None
    current_image = None
    
    # image handling
    current_image_pixmap = None
    current_scene = None
    
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.bind_connect()
    
    def open_folder(self):
        """
            Open a project folder
        """
        # Open Folder
        current_folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        
        # If not selected
        print(current_folder)
        if current_folder == None or current_folder == "":
            print("No folder was selected...")
            return
        else:
            self.current_folder = str(current_folder)
        
        # List Files
        self.listFile.addItems(utils.list_images(self.current_folder))


    def close_folder(self):
        """
            Handles File Menu "Close"
        """
        # Close the folder
        self.current_folder = None
        self.listFile.clear()
        self.img.setScene(QGraphicsScene())
        self.txtCaption.clear()
        
        # btn
        self.btnSaveCaption.setEnabled(False)
        
        # Status
        self.setStatusTip("Ready")
        
        
    
    
    def message(self, text):
        """
            Message
        """
        QMessageBox.information(self, "Info", text)
    
    
    def list_item_select(self, item):
        """
            Runs when the list item is clicked
        """
        # get file
        text = item.text()
        file_path = os.path.join(self.current_folder, text)
        
        # path
        if not os.path.exists(file_path):
            print("file not found")
            return
        
        self.current_image = file_path
        # load the image
        self.load_image()
        # render the new image
        self.render_scene()

    
    def load_image(self, url=None):
        """
            loads a image to a self.img_scene pixmap for rendering and renders
        """
        if url == None and not self.current_image == None: url=self.current_image
        else: return
        print("selected image: " + url)
        
        self.img.setAlignment(Qt.AlignCenter)
        
        # set
        self.current_image_pixmap = QPixmap(url)
        self.img_scene = QGraphicsScene()
        self.img_scene.addPixmap(self.current_image_pixmap)
        
        # btn
        self.btnSaveCaption.setEnabled(True)
        
        # load caption if exists
        self.load_caption()
    
    def render_scene(self):
        """
            Render self.img_scene without reloading the image
        """
        
        # Scene
        self.img.setScene(self.img_scene)
        
        # Scale
        self.img.fitInView(QRectF(0, 0, self.current_image_pixmap.width(), self.current_image_pixmap.height()), Qt.KeepAspectRatio)


    def resizeEvent(self, event):
        """
            Overrides the resize event
        """
        
        # render image everytime window resizes
        if self.current_image: self.render_scene()
        
        # resize
        QtWidgets.QMainWindow.resizeEvent(self, event)


    def load_caption(self, filename=None):
        """
            Load caption from txt if exits
        """
        # filename
        if filename == None:
            filename = os.path.join(self.current_folder, self.listFile.currentItem().text())
        
        # caption file
        caption_path = utils.change_file_ext(filename, "txt")
        
        # caption
        caption = None
        if os.path.exists(caption_path):
            caption = self.read_caption(caption_path)
        
        self.txtCaption.document().setPlainText(caption)


    def btn_save_caption_clicked(self):
        """
            Handles SaveCaption button click
        """
        # cap
        caption = self.txtCaption.document().toPlainText()
        
        # filename
        filename = os.path.join(self.current_folder, self.listFile.currentItem().text())

        # caption file
        caption_path = utils.change_file_ext(filename, "txt")
        
        self.save_caption(caption_path, caption)
    
    def save_caption(self, filename, caption):
        """
            Save the caption in a txt file
        """
        with open(filename, "w+") as file:
            file.write(caption)
        
        print(f"[+] {filename}")
        print("Saved caption...")

    def read_caption(self, filename):
        """
            Read the caption from a txt file
        """
        caption = None
        with open(filename, "r", encoding="utf-8", errors="ignore") as file:
            caption = file.read()
        
        return caption

    def choose_theme_dialog(self):
        """
            Show a choose theme dialog
        """
        dlg = ThemeChooseDlg()
        if dlg.exec_():
            values = dlg.getResult()
            QtWidgets.QApplication.setStyle(values)
            
            # save current settings
            with shelve.open("config") as settings:
                settings["current_style"] = values
            return

        else:
            print("no theme chosen")
            return

    
    def bind_connect(self):
        """
            Connection Binder
        """
        # Exit
        self.mnuExit.triggered.connect(sys.exit)
        # Folder Select
        self.mnuOpenFolder.triggered.connect(self.open_folder)
        # Folder Close
        self.mnuCloseFolder.triggered.connect(self.close_folder)
        # Theme
        self.mnuTheme.triggered.connect(self.choose_theme_dialog)
        
        # ListWidget
        self.listFile.itemClicked.connect(self.list_item_select)
        
        # Caption Button
        self.btnSaveCaption.clicked.connect(self.btn_save_caption_clicked)




if __name__ == "__main__":
    # check and read style
    current_style = None
    
    # read settings
    if os.path.exists("config.dat"):
        try:
            with shelve.open("config") as settings:
                if "current_style" in settings: current_style = settings["current_style"]
        except Exception as e:
            print(e)
        finally: pass

    # Run
    app = QtWidgets.QApplication(sys.argv)
    
    # Style
    # if current_style: app.setStyle(current_style)
    
    # Windows
    window = MainWindow()
    window.show()
    app.exec()
