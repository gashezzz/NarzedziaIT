import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from converter import convert

class ConvertThread(QThread):
    result = pyqtSignal(str)

    def __init__(self, input_path, output_path):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        try:
            convert(self.input_path, self.output_path)
            self.result.emit("File converted successfully")
        except Exception as e:
            self.result.emit(f"Failed to convert file: {e}")

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Data Converter')
        layout = QVBoxLayout()

        self.btnConvert = QPushButton('Convert File', self)
        self.btnConvert.clicked.connect(self.convert_file)
        layout.addWidget(self.btnConvert)

        self.setLayout(layout)
        self.resize(300, 100)

    def convert_file(self):
        options = QFileDialog.Options()
        input_path, _ = QFileDialog.getOpenFileName(self, 'Select input file', '', 'All Files (*);;JSON Files (*.json);;XML Files (*.xml);;YAML Files (*.yaml *.yml)', options=options)
        if input_path:
            output_path, _ = QFileDialog.getSaveFileName(self, 'Select output file', '', 'All Files (*);;JSON Files (*.json);;XML Files (*.xml);;YAML Files (*.yaml *.yml)', options=options)
            if output_path:
                self.thread = ConvertThread(input_path, output_path)
                self.thread.result.connect(self.show_message)
                self.thread.start()

    def show_message(self, message):
        QMessageBox.information(self, 'Result', message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConverterApp()
    ex.show()
    sys.exit(app.exec_())

