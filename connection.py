import os

from PyQt6 import QtWidgets, QtSql


class Connection:
    def db_conexion(self = None):
        ruta_db = './data/bbdd.sqlite'

        if not os.path.isfile(ruta_db):
            QtWidgets.QMessageBox.critical(None, 'Error', 'El archivo de la base de datos no existe.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(ruta_db)

        if db.open():
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                QtWidgets.QMessageBox.critical(None, 'Error', 'Base de datos vacía o no válida.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return False
            else:
                QtWidgets.QMessageBox.information(None, 'Aviso', 'Conexión Base de Datos realizada',
                                                  QtWidgets.QMessageBox.StandardButton.Ok)
                return True
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo abrir la base de datos.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

    def listProv(self=None):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM provincias;")
            list_prov = []

            if query.exec():
                while query.next():
                    list_prov.append(query.value(1))

                return list_prov

        except Exception as e:
            print("Error while fetching provinces form db ", e)

    @staticmethod
    def listMuniProv(province):
        try:
            listMunicipios = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM municipios where idprov = (select idprov from provincias where provincia = :province)")
            query.bindValue(":province", province)
            if query.exec():
                while query.next():
                    listMunicipios.append(query.value(1))
            return listMunicipios
        except Exception as e:
            print("error en cargar MuniProv", e)

    @staticmethod
    def getCustomers():
        listCustomers = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM customers WHERE historical = :false order by surname;")
        query.bindValue(":false", str(False))
        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(query.record().count())]
                listCustomers.append(row)
        return listCustomers



    @staticmethod
    def dataOneCustomer(data, key):
        try:
            customerData = []
            query = QtSql.QSqlQuery()
            match key:
                case "mobile":
                    query.prepare("SELECT * from customers where mobile= :mobile;")
                    query.bindValue(":mobile", str(data).strip())
                case "ID":
                    query.prepare("SELECT * from customers where dni_nie= :dni_nie;")
                    query.bindValue(":dni_nie", str(data).strip())

            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        customerData.append(query.value(i))
            return customerData
        except Exception as e:
            print("error en cargar dataOneCustomer", e)


    def deleteCustomer(dnicif):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers SET historical = :value WHERE dni_nie = :dnicif;")
            query.bindValue(":dnicif", dnicif)
            query.bindValue(":value", str(False))
            if query.exec():
                return True
            else:
                return False

        except Exception as error:
            print("Deleting connection method failed!", error)


    @staticmethod
    def addCustomer(newCli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO customers (dni_nie, adddata, surname, name, mail, mobile, address, province, city, invoicetype, historical) VALUES (:dni_nie, :adddata, :surname, :name, :mail, :mobile, :address, :province, :city, :invoicetype, :historical) ")
            query.bindValue(":dni_nie", str(newCli[0]))
            query.bindValue(":adddata", str(newCli[1]))
            query.bindValue(":surname", str(newCli[2]))
            query.bindValue(":name", str(newCli[3]))
            query.bindValue(":mail", str(newCli[4]))
            query.bindValue(":mobile", str(newCli[5]))
            query.bindValue(":address", str(newCli[6]))
            query.bindValue(":province", str(newCli[7]))
            query.bindValue(":city", str(newCli[8]))
            query.bindValue(":invoicetype", str(newCli[9]))
            query.bindValue(":historical", str(False))

            if query.exec():
                return True
            else:
                return False

        except Exception as error:
            print("error en cargar addCli", error)


    @staticmethod
    def alterCustomer(customerInfo):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "UPDATE customers SET dni_nie = :dni_nie, adddata = :adddata, surname = :surname, name = :name, mail = :mail, mobile = :mobile, address = :address, province = :province, city = :city, invoicetype = :invoicetype, historical = :historical WHERE dni_nie = :dni_nie;")

            valuePlaceholerList = [":dni_nie", ":adddata", ":surname", ":name", ":mail", ":mobile", ":address",
                                   ":province", ":city", ":invoicetype", ":historical"]
            for i in range(len(valuePlaceholerList)):
                query.bindValue(valuePlaceholerList[i], customerInfo[i])

            if query.exec():
                print("(Connection.alterCustomer) The next customer has been added: ", customerInfo)
                return True
            else:
                print("!!(Connection.alterCustomer) Query execution has failed! ", customerInfo)
                return False


        except Exception as error:
            print("!!(Connection.alterCustomer) Error saving the new customer! ", error)