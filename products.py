from PyQt6 import QtWidgets, QtCore

import conexion
import globals
from conexion import Conexion


class Products:
    # COmo cargar un combo desde un array
    def cargaFamilypro(self):
        familia = ["", "Foods", "Furniture", "Clothes", "Electronics"]
        globals.ui.cb_familia.clear()
        globals.ui.cb_familia.addItems(familia)


    @staticmethod
    def loadTableProduct():
        try:
            listProducts = Conexion.listProductos()

            index = 0
            for product in listProducts:
                globals.ui.table_productos.setRowCount(index + 1)
                globals.ui.table_productos.setItem(index, 0, QtWidgets.QTableWidgetItem(str(product[0])))
                globals.ui.table_productos.setItem(index, 1, QtWidgets.QTableWidgetItem(product[1]))
                globals.ui.table_productos.setItem(index, 2, QtWidgets.QTableWidgetItem(str(product[2])))
                globals.ui.table_productos.setItem(index, 4, QtWidgets.QTableWidgetItem(str(product[3])))
                globals.ui.table_productos.setItem(index, 3, QtWidgets.QTableWidgetItem(product[4]))

                globals.ui.table_productos.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.table_productos.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.table_productos.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.table_productos.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.table_productos.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)

                index += 1

        except Exception as e:
            print(e)

    def newProduct(self):
        try:
            newproduct = [globals.ui.le_nombre.text(),
                          globals.ui.le_stock.text(),
                          globals.ui.le_precio.text(),
                          globals.ui.cb_familia.currentText()]


            if Conexion.addProduct(newproduct):
                print("Product added successfully")
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Product added")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                    mbox.hide()
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Warning")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText("Warning, no Product added")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)
                    if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                        mbox.hide()
                Products.loadTableProduct()
        except Exception as e:
            print(e)

    @staticmethod
    def selectProduct():

        try:
            row = globals.ui.table_productos.selectedItems()
            data = [dato.text() for dato in row]
            record = Conexion.dataOneProduct(data[0])
            boxes = [globals.ui.le_codigo,
                     globals.ui.le_nombre,
                     globals.ui.le_stock,
                     globals.ui.le_precio
                     ]

            for i in range(len(boxes)):
                boxes[i].setText(str(record[i]))
            globals.ui.cb_familia.setCurrentText(str(record[4]))

        except Exception as error:
            print("error en selectProduct ", error)

    def delProducto(self):
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("WARNING")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Product?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Cancel)
            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:

                code = globals.ui.le_codigo.text()
                if Conexion.deleteProd(code):

                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Delete Product?")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No )
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

                else:
                    print("Something went wrong")
                Products.loadTableProduct()

            else:
                pass

        except Exception as error:
            print("error en deleting customer ", error)

    @staticmethod
    def cleanProd():
        try:
            formprod = [
                globals.ui.le_codigo,
                globals.ui.le_nombre,
                globals.ui.le_stock,
                globals.ui.le_precio
            ]

            # Limpar os LineEdit
            for dato in formprod:
                dato.setText("")

            # Limpar o ComboBox
            globals.ui.cb_familia.setCurrentText("")


        except Exception as error:
            print("error en buscaCli ", error)

    @staticmethod
    def modifyPro():
        try:
            if globals.ui.le_codigo.text() != "":
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Modify Data")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
                mbox.setText("Are you sure modify all data?")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                    id = globals.ui.le_codigo.text()
                    modpro = [globals.ui.le_nombre.text(), globals.ui.cb_familia.currentText(),
                              globals.ui.le_stock.text(), globals.ui.le_precio.text()
                              ]

                    if Conexion.modifyPro(id, modpro):
                        mbox = QtWidgets.QMessageBox()
                        mbox.setWindowTitle("Information")
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                        mbox.setText("Product modified")
                        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                        if mbox.exec():
                            mbox.hide()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("Error modifying data. Empty Data? ")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()
            Products.loadTableProduct()
        except Exception as error:
            print("error modify pro ", error)