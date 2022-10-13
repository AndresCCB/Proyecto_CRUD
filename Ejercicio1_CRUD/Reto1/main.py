##BY ACCBL (Andres C. Castro B.)

import sys
from tkinter import ttk
from tkinter import *

import sqlite3

"""
ARCHIVO MAIN DONDE REALMENTE FUNCIONA TODO, Y DONDE ESTA EL PROGREMA REAL :D
"""

class Producto:
    
    db_name = 'database.db'

    def __init__(self, window): #Tienen que ser dobles guiones bajos
        self.wind = window
        self.wind.title('Aplicacion de Productos')

        #Crear un Frame que sea contenedor
        frame = LabelFrame(self.wind, text = 'Registrar un nuevo producto')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20) #puede que en columns spaiin sea 5

        #Entradas (Inputs)
        Label(frame, text = 'Nombre').grid(row=1, column=0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row = 1, column = 1)

        Label(frame, text = 'Descripcion').grid(row=2, column=0)
        self.descripcion = Entry(frame)
        self.descripcion.grid(row = 2, column = 1)

        Label(frame, text = 'Id Proveedor').grid(row=3, column=0) ######por un choice
        self.id_proveedor = Entry(frame)
        self.id_proveedor.grid(row = 3, column = 1)

        #Boton para agregar producto
        ttk.Button(frame, text = 'Guardar Producto', command = self.add_producto).grid(row = 4, columnspan = 2, sticky= W +E)

        #Salida de mensajes
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 4, column = 0, columnspan = 2, sticky = W + E)

        #Tabla
        self.tree = ttk.Treeview(height = 10, columns = ('#0', '#1', '#2, #3'))
        self.tree.grid(row = 5, column = 0, columnspan = 2) #puede que en columns sea 1
        
        self.tree.heading('#0', text = 'Id Producto', anchor = CENTER)
        self.tree.heading('#1', text = 'Nombre ', anchor = CENTER)
        self.tree.heading('#2', text = 'Descripcion', anchor = CENTER)
        self.tree.heading('#3', text = 'Id Proveedor', anchor = CENTER)

        ttk.Button(text = 'ELIMINAR', command = self.delete_producto).grid(row = 6, column = 0, sticky = W+E)
        ttk.Button(text = 'EDITAR', command = self.edit_producto).grid(row = 6, column = 1, sticky = W+E)
        ttk.Button(text = 'SIGUIENTE', command = self.siguiente).grid(row = 6, column = 2, sticky = W+E)
        

        #Para llenar las filas de la tabla con el metodo creado abajo
        self.get_producto()

    def run_query(self, query, parameters = ()): #CONEXION A LA BASE DE DATOS
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def siguiente(self):
        self.tree.destroy()
        self.wind.destroy()
        window = Tk()
        application = Proveedor(window)
        window.mainloop()

    def get_producto(self):
        records = self.tree.get_children() #Obtener todos los datos que esten en la tabla, para limpiarlos o agregarlos
        for element in records: #Ciclo para limpiar la tabla
            self.tree.delete(element)

        #Consultar los datos
        query = 'SELECT * FROM Producto ORDER BY nombre_producto DESC'
        db_rows = self.run_query(query)

        #LLenar los datos en tabla
        for row in db_rows:
            #print(row) #imprime por consola los registros de la base de datos
            self.tree.insert('', 'end', text= row[0], values=( row[1], row[2], row[3])) #en el row[] se pone el numero de la columna que se quere mostrar de la base de datos

    def validation(self): #Una validacion de que los espacios no esten vacios
        return len(self.nombre.get()) != 0 and len(self.id_proveedor.get()) !=0
        
    def add_producto(self):

        #Utiliza la validacion para saber si se ha escrito algo o no en los espacios de input
        if self.validation():
            #Si hay algo escrito, para a agregar el producto
            query = 'INSERT INTO Producto VALUES(NULL, ?, ?, ?)'
            parameters = (self.nombre.get(), self.descripcion.get(), self.id_proveedor.get())
            self.run_query(query, parameters)

            #Muestra un mensaje de que se ha agregado bien el producto
            self.message['text'] = 'El producto {} ha sido agregado'.format(self.nombre.get())
            self.nombre.delete(0, END)
            self.descripcion.delete(0, END)
            self.id_proveedor.delete(0, END)
        else:
            #Sino hay nada escrito, mostrara el mensaje en pantalla
            self.message['text'] = 'El nombre y el id del proveedor son requeridos'

        self.get_producto()

    def delete_producto(self):

        #Limpiar los mensajes
        self.message['text'] = ''

        #Saber que dato esta seleccionado, sino selecciona ninguna, muestra el mensaje.
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor selecciona un registro'
            return

        #Eliminar en si un registro
        #primero obtener los valores
        nombre = self.tree.item(self.tree.selection())['values'][0]
        query = 'DELETE FROM Producto WHERE nombre_producto = ?'
        self.run_query(query,(nombre, ))

        #Mensaje de que se ha realizado
        self.message['text'] = 'El registro {} se ha eliminado exitosamente'.format(nombre)
        self.get_producto()

    def edit_producto(self):

        #Limpiar los mensajes
        self.message['text'] = ''

        #Saber que dato esta seleccionado, sino selecciona ninguna, muestra el mensaje.
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor selecciona un registro'
            return

        #Editar en si un registro
        #primero obtener los valores
        nombre = self.tree.item(self.tree.selection())['values'][0]
        descripcion = self.tree.item(self.tree.selection())['values'][1]
        id_proveedor = self.tree.item(self.tree.selection())['values'][2] #error tacitoc x2 mi lok
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Producto'

        #Datos antiguos
        #Nombre
        Label(self.edit_wind, text = 'Registro anterior').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = nombre), state = 'readonly').grid(row = 0, column = 2)
        #Descripcion
        Label(self.edit_wind, text = 'Descripcion Anterior').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = descripcion), state = 'readonly').grid(row = 2, column = 2)
        #Id Proveedor
        Label(self.edit_wind, text = 'Proveedor Anterior').grid(row = 4, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = id_proveedor), state = 'readonly').grid(row = 4, column = 2)

        #Datos nuevos
        #Nombre
        Label(self.edit_wind, text = 'Nombre nuevo').grid(row = 1, column = 1)
        nuevo_nombre = Entry(self.edit_wind)
        nuevo_nombre.grid(row = 1, column = 2)
        #Descripcion
        Label(self.edit_wind, text = 'Descripcion nueva').grid(row = 3, column = 1)
        nueva_descripcion = Entry(self.edit_wind)
        nueva_descripcion.grid(row = 3, column = 2)
        #Id_proveedor
        Label(self.edit_wind, text = 'Nuevo proveedor').grid(row = 5, column = 1)
        nuevo_id_proveedor = Entry(self.edit_wind)
        nuevo_id_proveedor.grid(row = 5, column = 2)

        Button(self.edit_wind, text = 'Actualizar', command = lambda : self.edit_registros(nuevo_nombre.get(), nombre, nueva_descripcion.get(), descripcion, nuevo_id_proveedor.get(), id_proveedor)).grid(row = 6, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_registros(self, nuevo_nombre, nombre, nueva_descripcion, descripcion, nuevo_id_proveedor, id_proveedor):
        #PARA HACER EN SI LA EDICION DEL PRODUCTO, CUANDO YA SE LE DE AL BOTON, algun error por aca maybe
        query = 'UPDATE Producto SET nombre_producto = ?, descripcion = ?, FK_id_proveedor = ? WHERE nombre_producto = ? AND descripcion = ? AND FK_id_proveedor = ?' #Comando para actulizar un registro en sql
        parameters = (nuevo_nombre, nueva_descripcion, nuevo_id_proveedor,   nombre, descripcion, id_proveedor) #parametros necesarios
        self.run_query(query, parameters)
        self.edit_wind.destroy()

        #Mensaje de que se ha realizado
        self.message['text'] = 'El registro {} ha sido actualizado exitosamente'.format(nombre)
        self.get_producto()

class Proveedor:

    db_name = 'database.db'

    def __init__(self, win): #Tienen que ser dobles guiones bajos
        self.wind = win
        self.wind.title('Aplicacion de Proveedor')

        #Crear un Frame que sea contenedor
        frame = LabelFrame(self.wind, text = 'Registrar un nuevo proveedor') #, text = 'Registrar un nuevo proveedor' no deja poner nombre :,v
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20) #puede que en columns spaiin sea 5

        #Entradas (Inputs)
        Label(frame, text = 'Nombre').grid(row=1, column=0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row = 1, column = 1)

        Label(frame, text = 'Direccion').grid(row=2, column=0)
        self.direccion = Entry(frame)
        self.direccion.grid(row = 2, column = 1)

        #Boton para agregar producto
        ttk.Button(frame, text = 'Guardar Proveedor', command = self.add_proveedor).grid(row = 3, columnspan = 2, sticky= W +E)

        #Tabla
        self.tree = ttk.Treeview(height = 10, columns = ('#0', '#1')) #Funciona ¿Como? NO c
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Id proveedor', anchor = CENTER)
        self.tree.heading('#1', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#2', text = 'Direccion', anchor = CENTER)

        Button(text = 'ELIMINAR', command = self.delete_proveedor).grid(row = 5, column = 0, sticky = W+E)
        Button(text = 'EDITAR', command = self.edit_proveedor).grid(row = 5, column = 1, sticky = W+E)
        Button(text = 'SIGUIENTE', command = self.siguiente).grid(row = 5, column = 2, sticky = W + E)

        #Salida de mensajes
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 4, column = 0, columnspan = 2, sticky = W + E)

        #Para llenar las filas de la tabla con el metodo creado abajo
        self.get_proveedor()                

    def run_query(self, query, parameters = ()): #CONEXION A LA BASE DE DATOS
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def siguiente(self):
        self.tree.destroy()
        self.wind.destroy()
        window = Tk()
        application = Producto(window)
        window.mainloop()
                

    def get_proveedor(self):
        registro = self.tree.get_children() #Obtener todos los datos que esten en la tabla, para limpiarlos o agregarlos
        for element in registro: #Ciclo para limpiar la tabla
            self.tree.delete(element)

        #Consultar los datos
        query = 'SELECT * FROM Proveedor ORDER BY nombre DESC'
        db_rows = self.run_query(query)

        #LLenar los datos en tabla
        for row in db_rows:
            self.tree.insert('', 'end', text= row[0], values=( row[1], row[2])) #en el row[] se pone el numero de la columna que se quere mostrar de la base de datos
            ##MAYOR ERROR ACA VIDA HPTA x2

    def validation(self): #Una validacion de que los espacios no esten vacios
        return len(self.nombre.get()) != 0 and len(self.direccion.get()) !=0
        
    def add_proveedor(self):

        #Utiliza la validacion para saber si se ha escrito algo o no en los espacios de input
        if self.validation():
            #Si hay algo escrito, para a agregar el producto
            query = 'INSERT INTO Proveedor VALUES(NULL, ?, ?)'
            parameters = (self.nombre.get(), self.direccion.get())
            self.run_query(query, parameters)

            #Muestra un mensaje de que se ha agregado bien el producto
            self.message['text'] = 'El Proveedor {} ha sido agregado'.format(self.nombre.get())
            self.nombre.delete(0, END)
            self.direccion.delete(0, END)
        else:
            #Sino hay nada escrito, mostrara el mensaje en pantalla
            self.message['text'] = 'El nombre y la direccion del proveedor son requeridos'

        self.get_proveedor()

    def delete_proveedor(self):

        #Limpiar los mensajes
        self.message['text'] = ''

        #Saber que dato esta seleccionado, sino selecciona ninguna, muestra el mensaje.
        try:
            self.tree.item(self.tree.selection())['values'][1]
        except IndexError as e:
            self.message['text'] = 'Por favor selecciona un registro'
            return

        #Eliminar en si un registro
        #primero obtener los valores
        nombre = self.tree.item(self.tree.selection())['values'][0] #Este cambia dado que values es el nombre, y el la lista valñues el nombre esta en la posicion 0
        query = 'DELETE FROM Proveedor WHERE nombre = ?'
        self.run_query(query,(nombre, ))

        #Mensaje de que se ha realizado
        self.message['text'] = 'El registro {} se ha eliminado exitosamente'.format(nombre)
        self.get_proveedor()

    def edit_proveedor(self):

        #Limpiar los mensajes
        self.message['text'] = ''

        #Saber que dato esta seleccionado, sino selecciona ninguna, muestra el mensaje.
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor selecciona un registro'
            return

        #Editar en si un registro
        #primero obtener los valores
        nombre = self.tree.item(self.tree.selection())['values'][0]
        direccion = self.tree.item(self.tree.selection())['values'][1]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar Proveedor'

        #Datos antiguos
        #Nombre
        Label(self.edit_wind, text = 'Nombre anterior').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = nombre), state = 'readonly').grid(row = 0, column = 2)
        #Descripcion
        Label(self.edit_wind, text = 'Direccion Anterior').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = direccion), state = 'readonly').grid(row = 2, column = 2)

        #Datos nuevos
        #Nombre
        Label(self.edit_wind, text = 'Nombre nuevo').grid(row = 1, column = 1)
        nuevo_nombre = Entry(self.edit_wind)
        nuevo_nombre.grid(row = 1, column = 2)
        #Direccion
        Label(self.edit_wind, text = 'Direccion nueva').grid(row = 3, column = 1)
        nueva_direccion = Entry(self.edit_wind)
        nueva_direccion.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Actualizar', command = lambda : self.edit_registro(nuevo_nombre.get(), nombre, nueva_direccion.get(), direccion)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_registro(self, nuevo_nombre, nombre, nueva_direccion, direccion):
        #PARA HACER EN SI LA EDICION DEL PRODUCTO, CUANDO YA SE LE DE AL BOTON, algun error por aca maybe
        query = 'UPDATE Proveedor SET nombre = ?, direccion = ? WHERE nombre = ? AND direccion = ?' #Comando para actulizar un registro en sql
        parameters = (nuevo_nombre, nueva_direccion, nombre, direccion) #parametros necesarios
        self.run_query(query, parameters)
        self.edit_wind.destroy()

        #Mensaje de que se ha realizado
        self.message['text'] = 'El registro {} ha sido actualizado exitosamente'.format(nombre)
        self.get_proveedor()

if __name__ == '__main__': #dobles guiones bajos

    def funcion(choice):
        if choice == 'Tabla Proveedor':
            funcion
        if choice == 'Tabla Producto':
            funcion

        while choice != 'Exit':
            ws.destroy()

            if choice ==  'Tabla Proveedor':
                window = Tk()
                application = Proveedor(window)
                window.mainloop()
            
            if choice == 'Tabla Producto':
                window = Tk()
                application = Producto(window)
                window.mainloop()
                
            if choice == 'Exit':
                break
        
        if choice == 'Exit':
            sys.exit(0)

    ws = Tk()
    ws.title('Menu')
    ws.geometry('280x80')

    eleccion = ['Exit', 'Tabla Proveedor','Tabla Producto']

    # setting variable for Integers
    variable = StringVar()
    variable.set(eleccion[2])

    # creating widget
    dropdown = OptionMenu(
        ws,
        variable,
        *eleccion,
        command = funcion
    )

    # positioning widget
    dropdown.grid(row = 0, column = 0, columnspan = 3, pady = 20)
    dropdown.config(width = 40 )

    # infinite loop 
    ws.mainloop()



    

        
        




    