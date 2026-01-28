from datetime import date

from PyQt6 import QtCore

import conexion
from conexion import *
import globals


class Invoice:

    @staticmethod
    def setInvoice():
        try:
            dni = globals.ui.lb_dni_cliente.text().upper().strip()

            if globals.ui.lb_dni_cliente.text() == "":
                dni = "00000000T"
            globals.ui.lb_dni_cliente.setText(dni)
            record = Conexion.dataOneCustomer(dni)
            if len(record) != 0:
                globals.ui.lb_dni_cliente.setText(record[0])
                globals.ui.lb_le_name_fact.setText(record[2] + '    ' + record[3])
                globals.ui.lb_le_tipo_fact.setText(record[9])
                globals.ui.lb_le_adress_fact.setText(record[6] + '    ' + record[8] + '    ' + record[7])
                globals.ui.lb_le_movil_fact.setText(record[5])
                if record[10]:
                    globals.ui.lb_le_status_fact.setText('Activo')
                else:
                    globals.ui.lb_le_status_fact.setText('Inactivo')
            else:
                globals.ui.lb_dni_cliente.setText("")
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Warning")
                mbox.setText("Customers do not Exist")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()

        except Exception as error:
            print("error en saveInvoice ", error)


    @staticmethod
    def cleanInvoice():
        try:
            formprod = [
                globals.ui.lb_le_name_fact,
                globals.ui.lb_le_adress_fact,
                globals.ui.lb_le_status_fact,
                globals.ui.lb_le_movil_fact,
                globals.ui.lb_le_tipo_fact
            ]
            # Limpar os LineEdit
            for dato in formprod:
                dato.setText("")
        except Exception as error:
            print("error en cleanInvoice ", error)



    def saveInvoice(self = None):

        try:

            dni = globals.ui.lb_dni_cliente.text()

            today = date.today().strftime("%d/%m/%Y")

            if conexion.Conexion.insertInvoice(dni, today):
                Invoice.loadTablefact()
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Invoice")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Invoice created successfully")
                if mbox.exec():
                    mbox.hide()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Warning")
                mbox.setText("Missing Fields or Data")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()

        except Exception as error:
            print("error en saveInvoice ", error)


    @staticmethod
    def loadTablefact():
        try:
            datos = conexion.Conexion.allInvoices()
            index = 0
            for record in datos:
                globals.ui.table_all_fact.setRowCount(index + 1)
                globals.ui.table_all_fact.setItem(index, 0, QtWidgets.QTableWidgetItem(record[0]))
                globals.ui.table_all_fact.setItem(index, 1, QtWidgets.QTableWidgetItem(record[1]))
                globals.ui.table_all_fact.setItem(index, 2, QtWidgets.QTableWidgetItem(record[2]))
                globals.ui.table_all_fact.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                globals.ui.table_all_fact.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                globals.ui.table_all_fact.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index += 1

        except Exception as error:
            print("error en loadTablefact ", error)

   # def loadFactFirst(self=None):
   #     try:
   #         globals.ui.txtDnifac.setText("00000000T")
   #         globals.ui.lblNumfac.setText("")
   #         globals.ui.lblFechafac.setText("")
   #         Invoice.buscaCli(self=None)
   #     except Exception as error:
   #         print("error load fac first", error)

    @staticmethod
    def selectInvoice():
        try:
            row = globals.ui.table_all_fact.selectedItems()
            datas = [dato.text() for dato in row]
            globals.ui.lb_num_fact.setText(datas[0])
            globals.ui.lb_dni_cliente.setText(datas[1])
            globals.ui.lb_fecha.setText(datas[2])

            Invoice.setInvoice()
            Invoice.activeSales()
        except Exception as error:
            print("error en selectInvoice ", error)


    @staticmethod
    def activeSales(row = None):
        try:
            if row is None:
                row = 0
                globals.ui.table_sales.setRowCount(1)
            else:
                if row >= globals.ui.table_sales.rowCount():
                    globals.ui.table_sales.setRowCount(row + 1)
            # Columna 0 (código)
            globals.ui.table_sales.setItem(row, 0, QtWidgets.QTableWidgetItem(""))
            globals.ui.table_sales.item(row, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            # Columna 2 (price)
            globals.ui.table_sales.setItem(row, 2, QtWidgets.QTableWidgetItem(""))
            # Columna 3 (cantidad)
            globals.ui.table_sales.setItem(row, 3, QtWidgets.QTableWidgetItem(""))
            globals.ui.table_sales.item(row, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            # Columna 4 (total)
            globals.ui.table_sales.setItem(row, 4, QtWidgets.QTableWidgetItem(""))
        except Exception as error:
            print("error en activeSales ", error)

    def cellChangedSales(self, item):
        try:
            iva=0.21
            row = item.row()
            col = item.column()
            if row == 0:
                subtotal = 0
            if col not in (0, 3):
                return

            value = item.text().strip()
            if value == "":
                return

            globals.ui.table_sales.blockSignals(True)

            # Columna 0 entonces buscar producto y rellenar nombre y precio
            if col == 0:
                subtotal = 0.00
                data = conexion.Conexion.selectProfducts(value)
                globals.ui.table_sales.setItem(row, 1, QtWidgets.QTableWidgetItem(str(data[0])))
                globals.ui.table_sales.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data[1])))
                globals.ui.table_sales.item(row, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            # Columna 3 → calcular total
            elif col == 3:
                cantidad = float(value)
                precio_item = globals.ui.table_sales.item(row, 2)
                if precio_item:
                    precio = float(precio_item.text())
                    tot = round(precio * cantidad, 2)
                    globals.ui.table_sales.setItem(row, 4, QtWidgets.QTableWidgetItem(str(tot)))
                    globals.ui.table_sales.item(row, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight
                                                                        | QtCore.Qt.AlignmentFlag.AlignVCenter)

            globals.ui.table_sales.blockSignals(False)

            # Comprobar si la fila actual está completa y añadir nueva fila
            if all([
                globals.ui.table_sales.item(row, 0) and globals.ui.table_sales.item(row, 0).text().strip(),
                globals.ui.table_sales.item(row, 1) and globals.ui.table_sales.item(row, 1).text().strip(),
                globals.ui.table_sales.item(row, 2) and globals.ui.table_sales.item(row, 2).text().strip(),
                globals.ui.table_sales.item(row, 3) and globals.ui.table_sales.item(row, 3).text().strip(),
                globals.ui.table_sales.item(row, 4) and globals.ui.table_sales.item(row, 4).text().strip()
            ]):
                next_row = globals.ui.table_sales.rowCount()
                Invoice.activeSales(row=next_row)
                globals.subtotal = globals.subtotal + tot
                totaliva = round(globals.subtotal * iva, 2)

                globals.ui.lblSubTotalInv.setText(str(globals.subtotal)+' €')
                globals.ui.lblIVAInv.setText(str(totaliva +' €'))
                total = round(globals.subtotal + totaliva, 2)
                globals.ui.lblTotalInv.setText(str(total)+' €')



        except Exception as error:
            print("Error en cellChangedSales:", error)
            globals.ui.table_sales.blockSignals(False)