import os

from PyQt6 import QtSql, QtWidgets



class Conexion:
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
        listProv = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")

        if query.exec():
            while query.next():
                listProv.append(query.value(1))
        return listProv


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
    def listProductos():
        listProductos = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM productos order by code")
        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(query.record().count())]
                listProductos.append(row)
        return listProductos


    @staticmethod
    def listCustomers(var):
        listCustomers = []
        if var:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers where historical = :true order by surname")
            query.bindValue(":true", str(True))
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    listCustomers.append(row)

        else:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers order by surname")

            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    listCustomers.append(row)



        return listCustomers

    @staticmethod
    def dataOneCustomer(data):
        try:
            list = []
            dato = str(data).strip()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * from customers where mobile= :dato")
            query.bindValue(":dato", dato)
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        list.append(query.value(i))
            if len(list) == 0:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * from customers where dni_nie= :dato")
                query.bindValue(":dato", str(dato))
                if query.exec():
                    while query.next():
                        for i in range(query.record().count()):
                            list.append(query.value(i))

            return list

        except Exception as e:
            print("error en cargar dataOneCustomer", e)

    @staticmethod
    def deleteCli(dni):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers set historical = :value WHERE dni_nie = :dni")
            query.bindValue(":dni", str(dni))
            query.bindValue(":value", str(False))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("error in delete", e)


    @staticmethod
    def addCli(newCli):

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
            query.bindValue(":historical", str(True))

            if query.exec():
                return True
            if not query.exec():
                print("ERROR SQL:", query.lastError().text())
                return False


        except Exception as error:
            print("error en cargar addCli", error)

    @staticmethod
    def modifCli(dni, modifiCli):
        try:
            if str(dni) == "":
                return False
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers SET adddata= :data, surname= :surname, name= :name, mail= :mail, mobile= :mobile, address= :address, province= :province,city= :city, invoicetype= :invoicetype, historical= :historical WHERE dni_nie = :dni")

            query.bindValue(":dni", str(dni))
            query.bindValue(":data", str(modifiCli[0]))
            query.bindValue(":surname", str(modifiCli[1]))
            query.bindValue(":name", str(modifiCli[2]))
            query.bindValue(":mail", str(modifiCli[3]))
            query.bindValue(":mobile", str(modifiCli[4]))
            query.bindValue(":address", str(modifiCli[5]))
            query.bindValue(":province", str(modifiCli[6]))
            query.bindValue(":city", str(modifiCli[7]))
            query.bindValue(":invoicetype", str(modifiCli[9]))
            query.bindValue(":historical", str(modifiCli[8]))



            if query.exec():

                return True
            else:
                return False
        except:
            print("error in modifyCli")

    @staticmethod
    def dataOneProduct(data):
        try:
            list = []
            dato = str(data).strip()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * from productos where code= :dato")
            query.bindValue(":dato", dato)
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        list.append(query.value(i))


            return list
        except:
            print("error in dataOneProduct")


    def addProduct(newproduct):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT INTO productos (name, stock, precio,family) VALUES (:name, :stock, :precio, :family) ")
            query.bindValue(":name", str(newproduct[0]))
            query.bindValue(":stock", int(newproduct[1]))
            query.bindValue(":precio", int(newproduct[2]))
            query.bindValue(":family", str(newproduct[3]))


            if query.exec():
                return True
            else:
                return False

        except Exception as error:
            print("error en cargar addCli", error)

    def modifyPro(id, modpro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE productos SET name= :name, stock = :stock, precio =:precio, family =:family where code = :id")
            query.bindValue(":id", int(id))
            query.bindValue(":name", str(modpro[0]))
            query.bindValue(":family", str(modpro[1]))
            query.bindValue(":stock", int(modpro[2]))
            query.bindValue(":precio", int(modpro[3]))
            if query.exec():
                print("manolo")
                return True
            else:
                return False
        except Exception as error:
            print("error modifyPro", error)

    def deleteProd(code):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE from productos where code= :code")
            query.bindValue(":code", code)
            if query.exec():
                print("se borra")
                return True
            else:
                return False
        except Exception as error:
            print("error en cargar addCli", error)

    @staticmethod
    def buscaCli(dni):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT dni_nie FROM customers WHERE dni_nie = :dni")
            query.bindValue(":dni", dni)

            if not query.exec():
                print("SQL Error:", query.lastError().text())
                return False
            if not query.next():
                return False
            valor = query.value(0)
            return valor not in (None, 0, "")

        except Exception as error:
            print("Error en buscaCli:", error)
            return False
    @staticmethod
    def insertInvoice(dni, today):

        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO invoices (dni, fecha) VALUES (:dni, :fecha)")
            query.bindValue(":dni", dni)
            query.bindValue(":fecha", today)
            if query.exec():
                return True
            else:
                print("SQL Error:", query.lastError().text())
                return False

        except Exception as e:
            print("error en insertInvoice", e)

    @staticmethod
    def allInvoices():
        try:
            datos = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM invoices order by idFactura DESC")
            if query.exec():
                while query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
                    datos.append(row)

            return datos
        except Exception as error:
            print("error en allInvoices ", error)


    @staticmethod
    def selectProducts(item):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT name, price from productos where id = :id")
            query.bindValue(":id", int(item))
            if query.exec():
                while query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
                return row
        except Exception as error:
            print("error en selectProducts ", error)