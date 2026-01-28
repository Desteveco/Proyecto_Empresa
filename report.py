import datetime
from logging import exception

from PIL import Image
from reportlab.pdfgen import canvas
import os
import globals
from conexion import Conexion


class Report():
    def __init__(self):
        rootPath= ".\\reports"
        data = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.namereportcli = data + "_reportcustomers.pdf"
        self.pdf_path = os.path.join(rootPath, self.namereportcli)
        self.c = canvas.Canvas(self.pdf_path)
        self.rootPath = rootPath

    def footer(self, title):

        try:

            self.c.line(35, 60, 525, 60)
            day = datetime.datetime.today()
            day = day.strftime("%d/%m/%Y %H:%M:%S")
            self.c.setFont("Helvetica", 7)
            self.c.drawString(70, 50, day)
            self.c.drawString(250, 50, title)
            self.c.drawString(500, 50, str("Page: " + str(self.c.getPageNumber())))

        except Exception as error:
            print(error)
    def topreport(self, title):
        try:
            path_logo = ".\\img\\logo.jpg"
            logo = Image.open(path_logo)
            if isinstance(logo, Image.Image):

                self.c.setFont("Helvetica", 10)
                self.c.drawString(55, 785, "EMPRESA TEIS")
                self.c.drawCentredString(300, 675, title)
                self.c.line(35, 665, 525, 665)
                self.c.drawImage(path_logo, 480, 745, 40, 40)
                # data company
                self.c.setFont("Helvetica", 8)
                self.c.drawString(55, 760, "CIF: A65327894")
                self.c.drawString(55, 745, "Avda de Galicia 101")
                self.c.drawString(55, 730, "Vigo - 36215 - España")
                self.c.drawString(55, 715, "Tlfo: 986 123 456")
                self.c.drawString(55, 700, "email:teis@mail.com")
                self.c.line(50, 800, 160, 800)
                self.c.line(50, 695, 160, 695)
                self.c.line(50, 800, 50, 695)
                self.c.line(160, 800, 160, 695)



            else:
                print("Cannot load image")
        except Exception as e:
            print(e)


    def reportCustomers(self):
        try:

            title = "List Client"
            self.footer(title)
            self.topreport(title)
            var = False
            records = Conexion.listCustomers(var)
            items = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATE"]
            self.c.setFont("Helvetica-Bold", 10)
            self.c.drawString(55, 650, items[0])
            self.c.drawString(120, 650, items[1])
            self.c.drawString(220, 650, items[2])
            self.c.drawString(270, 650, items[3])
            self.c.drawString(320, 650, items[4])
            self.c.drawString(400, 650, items[5])
            self.c.drawString(480, 650, items[6])
            self.c.line(40, 645, 555, 645)
            x = 55
            y = 630
            for record in records:
                if y <= 90:
                    self.c.setFont("Helvetica-Oblique", 8)
                    self.c.drawString(55, 75, "Next Page")
                    self.c.showPage() #Crea una nueva página
                    self.items = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATE"]
                    self.c.setFont("Helvetica-Bold", 10)
                    self.c.drawString(55, 650, items[0])
                    self.c.drawString(120, 650, items[1])
                    self.c.drawString(220, 650, items[2])
                    self.c.drawString(270, 650, items[3])
                    self.c.drawString(320, 650, items[4])
                    self.c.drawString(400, 650, items[5])
                    self.c.drawString(480, 650, items[6])
                    self.c.line(50, 645, 545, 645)
                    x = 55
                    y = 630
                self.c.setFont("Helvetica", 8)
                dni = "*****" + record[0][-4:]
                self.c.drawString(x, y, dni)
                self.c.drawString( x + 65, y, record[2])
                self.c.drawString( x + 165, y, record[3])
                self.c.drawString( x + 215, y, record[5])
                self.c.drawString( x + 265, y, record[8])
                self.c.drawString( x + 345, y, record[9])
                if record[10]:
                    self.c.drawString( x + 425, y, "Alta")
                else:
                    self.c.drawString( x + 425, y, "Baja")
                y -= 25
            self.c.save()
            for file in os.listdir(self.rootPath):
                if file.endswith(self.namereportcli):
                    os.startfile(self.pdf_path)
        except Exception as e:
            print(e)



    def ticket(self):
        try:
            dni = globals.ui.lb_dni_cliente.text()
            if dni == "00000000T":
                titulo = "FACTURA SIMPLIFICADA"
            else:
                titulo = "FACTURA"
            records = Conexion.dataOneCustomer(dni)
            print(records)
            self.c.setFont("Helvetica", 8)
            self.topreport(titulo)
            self.footer(titulo)

        except exception as e:
            print(e)
