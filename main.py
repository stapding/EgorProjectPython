import json
import socket
import sys
from datetime import datetime
from json import JSONDecodeError

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import threading
from dataclass import Order


class ServerSignals(QObject):
    new_data = pyqtSignal(object)


class ServerThread(threading.Thread):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals

    def run(self):
        self.start_server(self.signals)

    def start_server(self, signals, host='127.0.0.1', port=12345):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen()
        print(f"Server listening on {host}:{port}")

        try:
            while True:
                conn, addr = server.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr, signals))
                client_thread.start()
        except KeyboardInterrupt:
            print("Server is shutting down")
        finally:
            server.close()

    def handle_client(self, connection, address, signals):
        print(f"Connected by {address}")
        try:
            while True:
                data = connection.recv(10024)
                if not data:
                    break

                # Обработка данных
                received_data = ServerThread.decode(data)

                # Отправка данных в основной поток через сигнал
                signals.new_data.emit(received_data)

        except Exception as e:
            print(f"Error handling data from {address}: {e}")
        finally:
            connection.close()

    @staticmethod
    def decode(str1):
        try:
            received_json = str1.decode('utf-8')
            received_data = json.loads(received_json)
            return Order.deserializer(received_data)
        except JSONDecodeError:
            return None


class MyWindow(QtWidgets.QWidget):
    products = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Calculator")

        self.model = QStandardItemModel()
        self.model.setColumnCount(1)
        self.model.setHorizontalHeaderLabels(["Id", "Date", "Time", "User", "Value"])
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.clicked.connect(self.on_click)
        # Set column headers
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.clndr = QCalendarWidget(self)
        self.clndr.selectionChanged.connect(self.changeDate)

        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.table, 2, 0, 1, 1)
        self.grid.addWidget(self.clndr, 1, 0)

        self.start_server()

        self.data = list()
        self.data1 = list()

        self.setLayout(self.grid)

    @staticmethod
    def filterData(item,datet2):
        date1 = item.date
        datet = datetime.strptime(date1[:date1.index("T")], '%Y-%m-%d').date()
        return datet>datet2

    @staticmethod
    def filtered(data,selectedDate):
        return filter(lambda i: MyWindow.filterData(i,selectedDate), data)

    def changeDate(self):
        self.model.removeRows(0, self.model.rowCount())
        newData = MyWindow.filtered(self.data1,self.clndr.selectedDate().toPyDate())
        for i in newData:
            self.load_data(i)

    def start_server(self):
        self.server_signals = ServerSignals()

        self.server_signals.new_data.connect(self.load_data1)

        self.server_thread = ServerThread(self.server_signals)
        self.server_thread.start()

    def load_data1(self,data):
        self.data1.append(data)
        self.load_data(data)

    def load_data(self, data):
        self.data.append(data.products)
        sum = 0
        for i in data.products:
            sum += i.Price * i.Count

        order_date = data.date

        row = [
            QStandardItem(str(data.id)),
            QStandardItem(order_date[:order_date.index("T")]),
            QStandardItem(order_date[order_date.index("T") + 1:order_date.index(".")]),
            QStandardItem(data.get("user").get("Name")),
            QStandardItem(str(sum))
        ]

        for i in row:
            i.setEditable(False)

        self.model.appendRow(row)

    @pyqtSlot(QModelIndex)
    def on_click(self, index):
        for i in range(len(self.data)):
            if i == index.row():
                self.products.emit(self.data[i])
        self.parent().setCurrentIndex(1)


class MyWindow2(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.layout = QVBoxLayout()
        self.button = QPushButton("Go back")
        self.button.clicked.connect(self.go_back)

        self.model = QStandardItemModel()
        self.model.setColumnCount(1)
        self.model.setHorizontalHeaderLabels(["Id", "Name", "Count", "Price"])
        self.table = QTableView()
        self.table.setModel(self.model)
        # Set column headers
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.grid = QtWidgets.QGridLayout()
        self.grid.addWidget(self.table, 2, 0, 1, 1)

        self.search = QLineEdit()
        self.search.textChanged.connect(self.onSearchChanged)

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.search)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.products = None

    def getProducts(self, products):
        if self.products is None:
            self.products = products

        for item in products:
            row = [
                QStandardItem(str(item.Id)),
                QStandardItem(item.Name),
                QStandardItem(str(item.Count)),
                QStandardItem(str(item.Price))
            ]
            for i in row:
                i.setEditable(False)
            self.model.appendRow(row)

    @pyqtSlot()
    def go_back(self):
        self.model.removeRows(0, self.model.rowCount())
        self.parent().setCurrentIndex(0)

    @staticmethod
    def search(data,text):
        searchProducts = data
        if text != "":
            searchProducts = filter(lambda p: text in p.Name.lower(), data)
        return searchProducts

    def onSearchChanged(self,text):
        self.model.removeRows(0, self.model.rowCount())

        searchProducts = MyWindow2.search(self.products,text)


        for item in searchProducts:
            row = [
                QStandardItem(str(item.Id)),
                QStandardItem(item.Name),
                QStandardItem(str(item.Count)),
                QStandardItem(str(item.Price))
            ]
            for i in row:
                i.setEditable(False)
            self.model.appendRow(row)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QStackedWidget()
    widget = MyWindow()
    widget2 = MyWindow2()
    widget.products.connect(widget2.getProducts)
    window.addWidget(widget)
    window.addWidget(widget2)
    window.show()
    sys.exit(app.exec_())
