import tkinter as tk
from tkinter import *
from tkinter import ttk, END
import sys
import time
import calendar
import random
import datetime as dt
import sqlite3
from tkinter import messagebox

LARGE_FONT = ("Copperplate Gothic Bold", 12)


class ImsCoffee(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Inventory Management System")
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Supplies, Supplier, Inventory, Menu):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Menu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Supplies(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Supplies", font=LARGE_FONT, bg="#98EFDA")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=50, sticky='w')

        """button = tk.Button(self, text="Visit Page 1",
                           command=lambda: controller.show_frame(PageOne))
        button.grid(row=2, column=0,)

        button2 = tk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.grid(row=3, column=0,)"""
        def dbSetup2():
            # initiate or connects data base
            connect = sqlite3.connect('IMS.db')
            cursor = connect.cursor()
            # create table
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS "Coffee"(
                    coffee_id VARCHAR(4),
                    quantity INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    PRIMARY KEY (coffee_id)

                    )
                """)

            cursor.execute("""CREATE TABLE IF NOT EXISTS "Coffee_Components"(
            coffee_id varchar(4),
            component_number INT,
            component_name TEXT,
            quantity INT)
            """)

            connect.close()

        def dbSetup():
            # initiate or connects data base
            connect = sqlite3.connect('IMS.db')
            cursor = connect.cursor()
            # create table
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS "Orders"(
                    time INT NOT NULL,
                    date TEXT NOT NULL,
                    order_unit INT NOT NULL,
                    quantity TEXT NOT NULL
                    )
                """)

            connect.close()

        def displaydata():
            conn = sqlite3.connect('IMS.db')

            c = conn.cursor()

            c.execute("SELECT * FROM Orders")
            records = c.fetchall()

            global count
            count = 0

            for record in records:
                if count % 2 == 0:
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2],
                                                                                       record[3], record[4],
                                                                                       record[5], record[6]),
                                   tags=('evenrow',))
                else:
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2],
                                                                                       record[3], record[4],
                                                                                       record[5], record[6]),
                                   tags=('oddrow',))
                count += 1

            return

        def delete_data():
            for record in my_tree.get_children():
                my_tree.delete(record)

        def add():
            if itemname_entry.get() == '':
                return messagebox.showwarning("Warning!", "You haven't inputted anything")
            elif supname_entry.get() == '':
                return messagebox.showwarning("Warning!", "You haven't inputted anything")
            elif eprice.get() == '':
                return messagebox.showwarning("Warning!", "You haven't inputted anything")
            elif equantity.get() == '':
                return messagebox.showwarning("Warning!", "You haven't inputted anything")
            elif eunit.get() == '':
                return messagebox.showwarning("Warning!", "You haven't inputted anything")


            # connect the database
            conn = sqlite3.connect('IMS.db')
            c = conn.cursor()

            # Gets date from host computer.
            date = dt.datetime.now()
            # Takes the date and formats it.
            format_date = f"{date:%b %d %Y}"
            # Takes the current time
            current_time = date.strftime("%H:%M:%S")

            c.execute("INSERT INTO Orders VALUES (:item_name, :supplier_name, :price, :time, :date, "
                      ":quantity, :unit)",
                      {
                          'item_name': itemname_entry.get(),
                          'supplier_name': supname_entry.get(),
                          'price': eprice.get(),
                          'time': current_time,
                          'date': format_date,
                          'quantity': equantity.get(),
                          'unit': eunit.get(),
                      }
                      )

            # Commit changes
            conn.commit()

            # Close Connection
            conn.close()

            delete_data()
            displaydata()

            return

        def update():

            # Gets date from host computer.
            date = dt.datetime.now()
            # Takes the date and formats it.
            format_date = f"{date:%b %d %Y}"
            # Takes the current time
            current_time = date.strftime("%H:%M:%S")

            conn = sqlite3.connect('IMS.db')
            c = conn.cursor()
            data1 = itemname_entry.get()
            data2 = supname_entry.get()
            data3 = eprice.get()
            data4 = equantity.get()
            data5 = eunit.get()

            selected = my_tree.selection()
            my_tree.item(selected, values=(data1, data2, data3, data4))
            c.execute(
                "UPDATE Orders set  item_name=?, supplier_name=?, price=?, quantity=?, unit=?",
                (data1, data2, data3, data4, data5))

            conn.commit()
            conn.close()

            delete_data()
            displaydata()

        def delete():
            if not messagebox.askyesno("Delete Confirmation", "Are you sure?"):
                return
            else:
                conn = sqlite3.connect("IMS.db")
                c = conn.cursor()
                selected = my_tree.focus()
                values = my_tree.item(selected, 'values')

                c.execute("DELETE from Orders where time=?", (values[3],))

                conn.commit()
                conn.close()

            delete_data()
            displaydata()

        def clear():
            itemname_entry.delete(0, END)
            supname_entry.delete(0, END)
            eprice.delete(0, END)
            equantity.delete(0, END)
            eunit.delete(0, END)

        def select_record(e):
            itemname_entry.delete(0, END)
            supname_entry.delete(0, END)
            eprice.delete(0, END)
            equantity.delete(0, END)
            eunit.delete(0, END)

            pick = my_tree.focus()
            value = my_tree.item(pick, 'value')

            itemname_entry.insert(0, value[0])
            supname_entry.insert(0, value[1])
            eprice.insert(0, value[2])
            equantity.insert(0, value[5])
            eunit.insert(0, value[6])


        # add database
        dbSetup()
        # Create Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading",font=(None, 10))

        # style.configure("Treeview", rowheight="30")
        # Coffee TreeView
        # Frame for TreeView and scroll
        tree_frame = tk.Frame(self)
        tree_frame.grid(row=1, column=0, columnspan=6, padx=20, pady=10)

        # scroll
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Add TreeView
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, height=12)

        # Defining Columns
        my_tree['columns'] = ('Item Name', 'Supplier Name', 'Price', 'Time', 'Date', 'Qty', 'Unit')

        # Formatting Column
        my_tree.column("#0", stretch=tk.NO, width=0)
        my_tree.column("Item Name", width=125, anchor=tk.W)
        my_tree.column("Supplier Name", width=140, anchor=tk.W)
        my_tree.column("Price", width=75, anchor=tk.W)
        my_tree.column("Time", width=100, anchor=tk.W)
        my_tree.column("Date", width=100, anchor=tk.W)
        my_tree.column("Qty", width=50, anchor=tk.W)
        my_tree.column("Unit", width=75, anchor=tk.W)

        # Create Headings
        my_tree.heading("Item Name", text='Item Name', anchor=tk.CENTER)
        my_tree.heading("Supplier Name", text='Supplier Name', anchor=tk.CENTER)
        my_tree.heading("Price", text='Price', anchor=tk.CENTER)
        my_tree.heading("Time", text='Time', anchor=tk.CENTER)
        my_tree.heading("Date", text='Date', anchor=tk.CENTER)
        my_tree.heading("Qty", text='Qty', anchor=tk.CENTER)
        my_tree.heading("Unit", text='Unit', anchor=tk.CENTER)

        # Display TreeView
        my_tree.pack()

        # configure scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Frame for upper buttons
        upperSide = tk.Frame(self)
        upperSide.grid(row=0, column=2, columnspan=4, sticky='e')

        # upperSide buttons
        his_btn = tk.Button(upperSide, text="Supplier", font=LARGE_FONT,
                            command=lambda: controller.show_frame(Supplier))
        his_btn.grid(row=0, column=0, padx=10)

        inv_btn = tk.Button(upperSide, text="Inventory", font=LARGE_FONT,
                            command=lambda: controller.show_frame(Inventory))
        inv_btn.grid(row=0, column=1, padx=10)

        menu_btn = tk.Button(upperSide, text="Menu", font=LARGE_FONT, command=lambda: controller.show_frame(Menu))
        menu_btn.grid(row=0, column=2, padx=10)

        #list for inventory names and supplier names
        ex = sqlite3.connect('IMS.db')
        x = ex.cursor()

        x.execute("SELECT item_name FROM Inventory")
        rec = x.fetchall()
        itemname = []
        for i in rec:
            itemname.append(i[0])

        x.execute("SELECT supplier_name from Supplier")
        rec2=x.fetchall()
        suppliername = []
        for i in rec2:
            suppliername.append(i[0])


        # Entries and Labels
        # Frame for ^
        lower = tk.Frame(self)
        lower.grid(row=2, column=0, columnspan=8)

        itemname_lbl = tk.Label(lower, text="Item Name")
        itemname_lbl.grid(row=0, column=0)
        supname_lbl = tk.Label(lower, text="Supplier Name")
        supname_lbl.grid(row=0, column=2)
        price = tk.Label(lower, text="Price")
        price.grid(row=1, column=0)
        quantity = tk.Label(lower, text="Quantity")
        quantity.grid(row=1, column=2)
        unit = tk.Label(lower, text="Unit")
        unit.grid(row=0, column=4)

        # itemname_entry = tk.Entry(lower)
        # itemname_entry.grid(row=0, column=1, padx=5)

        itemname_entry = ttk.Combobox(lower, width=18)
        itemname_entry.set("Select Item")
        itemname_entry['values'] = itemname  # ("BSCS", "BSIT", "BSBA-B.ECON")
        itemname_entry.grid(row=0, column=1)

        # supname_entry = tk.Entry(lower)
        # supname_entry.grid(row=0, column=3)

        supname_entry = ttk.Combobox(lower, width=18)
        supname_entry.set("Select Supplier")
        supname_entry['values'] = suppliername  # ("BSCS", "BSIT", "BSBA-B.ECON")
        supname_entry.grid(row=0, column=3)

        eprice = tk.Entry(lower)
        eprice.grid(row=1, column=1)
        equantity = tk.Entry(lower)
        equantity.grid(row=1, column=3)

        #eunit = tk.Entry(lower)
        #eunit.grid(row=0, column=5)

        eunit = ttk.Combobox(lower, width=18)
        eunit.set("Select Unit")
        eunit['values'] = ("Kilo", "Grams", "Liter", "Stick")
        eunit.grid(row=0, column=5)


        add = tk.Button(lower, text="Add Order", font=LARGE_FONT, command=add)
        add.grid(row=2, column=0, padx=4, pady=5)
        modify = tk.Button(lower, text="Update", font=LARGE_FONT, command=update)
        modify.grid(row=2, column=1, padx=4)
        delete = tk.Button(lower, text="Delete", font=LARGE_FONT, command=delete)
        delete.grid(row=2, column=2, padx=4)
        clear = tk.Button(lower, text="Clear", font=LARGE_FONT, command=clear)
        clear.grid(row=2, column=3, padx=4)

        displaydata()

        my_tree.bind("<ButtonRelease-1>", select_record)


class Supplier(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def dbSetup():
            # initiate or connects data base
            connect = sqlite3.connect('IMS.db')
            cursor = connect.cursor()
            # create table
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS "Supplier"(
                    supplier_id INT,
                    supplier_name TEXT NOT NULL,
                    contact_number INT,
                    address TEXT NOT NULL,
                    PRIMARY KEY (supplier_id)

                    )
                """)
            connect.close()

        def displaydata():
            conn = sqlite3.connect('IMS.db')

            c = conn.cursor()

            c.execute("SELECT * FROM Supplier")
            records = c.fetchall()

            global count
            count = 0

            for record in records:
                if count % 2 == 0:
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2],
                                                                                       record[3]),
                                   tags=('evenrow',))
                else:
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2],
                                                                                       record[3]),
                                   tags=('oddrow',))
                count += 1

            return

        def delete_data():
            for record in my_tree.get_children():
                my_tree.delete(record)

        def add():
            if supid_entry.get() == '':
                return messagebox.showwarning("Warning!", "You haven't inputted anything")
            elif supname_entry.get() == '':
                return messagebox.showwarning("Warning!", "You haven't inputted anything")
            elif contact_entry.get() == '':
                return messagebox.showwarning("Warning!", "You haven't inputted anything")
            elif address_entry.get() == '':
                return messagebox.showwarning("Warning!", "You haven't inputted anything")

            # connect the database
            conn = sqlite3.connect('IMS.db')
            c = conn.cursor()

            c.execute("INSERT INTO Supplier VALUES (:supplier_id, :supplier_name, :contact_number, :address)",
                      {
                          'supplier_id': supid_entry.get(),
                          'supplier_name': supname_entry.get(),
                          'contact_number': contact_entry.get(),
                          'address': address_entry.get(),
                      }
                      )

            # Commit changes
            conn.commit()

            # Close Connection
            conn.close()

            delete_data()
            displaydata()

            return

        def update():

            conn = sqlite3.connect('IMS.db')
            c = conn.cursor()
            data1 = supid_entry.get()
            data2 = supname_entry.get()
            data3 = contact_entry.get()
            data4 = address_entry.get()

            selected = my_tree.selection()
            my_tree.item(selected, values=(data1, data2, data3, data4))
            c.execute(
                "UPDATE Supplier set  supplier_id=?, supplier_name=?, contact_number=?, address=? WHERE supplier_id=?",
                (data1, data2, data3, data4, data1))

            conn.commit()
            conn.close()

            delete_data()
            displaydata()

        def delete():
            if not messagebox.askyesno("Delete Confirmation", "Are you sure?"):
                return
            else:
                conn = sqlite3.connect("IMS.db")
                c = conn.cursor()
                selected = my_tree.focus()
                values = my_tree.item(selected, 'values')

                c.execute("DELETE from Supplier WHERE supplier_id=?", (values[0],))

                conn.commit()
                conn.close()

            delete_data()
            displaydata()

        def clear():
            supid_entry.delete(0, END)
            supname_entry.delete(0, END)
            contact_entry.delete(0, END)
            address_entry.delete(0, END)

        def select_record(e):
            supid_entry.delete(0, END)
            supname_entry.delete(0, END)
            contact_entry.delete(0, END)
            address_entry.delete(0, END)

            pick = my_tree.focus()
            value = my_tree.item(pick, 'value')

            supid_entry.insert(0, value[0])
            supname_entry.insert(0, value[1])
            contact_entry.insert(0, value[2])
            address_entry.insert(0, value[3])



        label = tk.Label(self, text="Supplier", font=LARGE_FONT, bg="#98EFDA")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=40, sticky='w')

        # Frame for table

        # Student TreeView
        # Frame for TreeView and scroll
        tree_frame = tk.Frame(self)
        tree_frame.grid(row=1, column=0, columnspan=6, padx=20, pady=10)

        # scroll
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Add TreeView
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, height=12)

        # Defining Columns
        my_tree['columns'] = ('SupplierID', 'Supplier Name', 'Contact No.', 'Address')

        # Formatting Column
        my_tree.column("#0", stretch=tk.NO, width=0)
        my_tree.column("SupplierID", width=80, anchor=tk.W)
        my_tree.column("Supplier Name", width=150, anchor=tk.W)
        my_tree.column("Contact No.", width=125, anchor=tk.W)
        my_tree.column("Address", width=300, anchor=tk.W)

        # Create Headings
        my_tree.heading("SupplierID", text='SupplierID', anchor=tk.CENTER)
        my_tree.heading("Supplier Name", text='Supplier Name', anchor=tk.CENTER)
        my_tree.heading("Contact No.", text='Contact No.', anchor=tk.CENTER)
        my_tree.heading("Address", text='Address', anchor=tk.CENTER)


        # Display TreeView
        my_tree.pack()

        # configure scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Frame for upper buttons
        upperSide = tk.Frame(self)
        upperSide.grid(row=0, column=2, columnspan=4, sticky='e')

        # upperSide buttons
        men_btn = tk.Button(upperSide, text="Supplies", font=LARGE_FONT, command=lambda: controller.show_frame(Supplies))
        men_btn.grid(row=0, column=0, padx=10)

        inv_btn = tk.Button(upperSide, text="Inventory", font=LARGE_FONT,
                            command=lambda: controller.show_frame(Inventory))
        inv_btn.grid(row=0, column=1, padx=10)

        ord_btn = tk.Button(upperSide, text="Menu", font=LARGE_FONT, command=lambda: controller.show_frame(Menu))
        ord_btn.grid(row=0, column=2, padx=10)

        # Entries and Labels
        # Frame for ^
        lower = tk.Frame(self)
        lower.grid(row=2, column=0, columnspan=8)

        supid_lbl = tk.Label(lower, text="SupplierID")
        supid_lbl.grid(row=0, column=0)
        supname_lbl = tk.Label(lower, text="Supplier Name")
        supname_lbl.grid(row=0, column=2)
        contact_lbl = tk.Label(lower, text="Contact No.")
        contact_lbl.grid(row=1, column=0)
        address_lbl = tk.Label(lower, text="Address")
        address_lbl.grid(row=1, column=2)

        supid_entry = tk.Entry(lower)
        supid_entry.grid(row=0, column=1, padx=5)
        supname_entry = tk.Entry(lower)
        supname_entry.grid(row=0, column=3)
        contact_entry = tk.Entry(lower)
        contact_entry.grid(row=1, column=1)
        address_entry = tk.Entry(lower)
        address_entry.grid(row=1, column=3)

        add = tk.Button(lower, text="Add Supplier", font=LARGE_FONT, command=add)
        add.grid(row=2, column=0, padx=4, pady=5)
        modify = tk.Button(lower, text="Update", font=LARGE_FONT, command=update)
        modify.grid(row=2, column=1, padx=4)
        delete = tk.Button(lower, text="Delete", font=LARGE_FONT, command=delete)
        delete.grid(row=2, column=2, padx=4)
        clear = tk.Button(lower, text="Clear", font=LARGE_FONT, command=clear)
        clear.grid(row=2, column=3, padx=4)

        dbSetup()
        displaydata()

        my_tree.bind("<ButtonRelease-1>", select_record)



class Inventory(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Inventory", font=LARGE_FONT, bg="#98EFDA")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=40, sticky='w')

        def dbSetup():
            # initiate or connects data base
            connect = sqlite3.connect('IMS.db')
            cursor = connect.cursor()
            # create table
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS "Inventory"(
                    item_code INT,
                    item_name TEXT NOT NULL,
                    quantity INT,
                    unit TEXT NOT NULL,
                    PRIMARY KEY (item_code)

                    )
                """)

            connect.close()

        def displaydata():
            conn = sqlite3.connect('IMS.db')

            c = conn.cursor()

            c.execute("SELECT * FROM Inventory")
            records = c.fetchall()

            global count
            count = 0

            for record in records:
                if count % 2 == 0:
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2],
                                                                                       record[3]),
                                   tags=('evenrow',))
                else:
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2],
                                                                                       record[3]),
                                   tags=('oddrow',))
                count += 1

            return

        def delete_data():
            for record in my_tree.get_children():
                my_tree.delete(record)

        def add():
            if centry.get() == '':
                return messagebox.showwarning("Warning!", "You haven't inputted anything")
            elif tentry.get() == '':
                return messagebox.showwarning("Warning!", "You haven't inputted anything")
            elif nentry.get() == '':
                return messagebox.showwarning("Warning!", "You haven't inputted anything")
            elif qty2.get() == '':
                return messagebox.showwarning("Warning!", "You haven't inputted anything")

            # connect the database
            conn = sqlite3.connect('IMS.db')
            c = conn.cursor()

            c.execute("INSERT INTO Inventory VALUES (:item_code, :item_type, :item_name, :quantity)",
                      {
                          'item_code': centry.get(),
                          'item_type': tentry.get(),
                          'item_name': nentry.get(),
                          'quantity': qty2.get(),
                      }
                      )

            # Commit changes
            conn.commit()

            # Close Connection
            conn.close()

            delete_data()
            displaydata()

            return

        def update():

            conn = sqlite3.connect('IMS.db')
            c = conn.cursor()
            data1 = centry.get()
            data2 = tentry.get()
            data3 = nentry.get()
            data4 = qty2.get()

            selected = my_tree.selection()
            my_tree.item(selected, values=(data1, data2, data3, data4))
            c.execute(
                "UPDATE Inventory set  item_code=?, item_type=?, item_name=?, quantity=? WHERE item_code=?",
                (data1, data2, data3, data4, data1))

            conn.commit()
            conn.close()

            delete_data()
            displaydata()

        def delete():
            if not messagebox.askyesno("Delete Confirmation", "Are you sure?"):
                return
            else:
                conn = sqlite3.connect("IMS.db")
                c = conn.cursor()
                selected = my_tree.focus()
                values = my_tree.item(selected, 'values')

                c.execute("DELETE from Inventory WHERE item_code=?", (values[0],))

                conn.commit()
                conn.close()

            delete_data()
            displaydata()

        def clear():
            centry.delete(0, END)
            tentry.delete(0, END)
            nentry.delete(0, END)
            qty2.delete(0, END)

        def select_record(e):
            centry.delete(0, END)
            tentry.delete(0, END)
            nentry.delete(0, END)
            qty2.delete(0, END)

            pick = my_tree.focus()
            value = my_tree.item(pick, 'value')

            centry.insert(0, value[0])
            tentry.insert(0, value[1])
            nentry.insert(0, value[2])
            qty2.insert(0, value[3])


        # connect to database
        dbSetup()

        # display data for inventory table
        #delete_data()


        # Frame for table

        # Student TreeView
        # Frame for TreeView and scroll
        tree_frame = tk.Frame(self)
        tree_frame.grid(row=1, column=0, columnspan=6, padx=20, pady=10)

        # scroll
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Add TreeView
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, height=12)

        # Defining Columns
        my_tree['columns'] = ('Item Code', 'Item Type', 'Name', 'Quantity')

        # Formatting Column
        my_tree.column("#0", stretch=tk.NO, width=0)
        my_tree.column("Item Code", width=160, anchor=tk.W)
        my_tree.column("Item Type", width=160, anchor=tk.W)
        my_tree.column("Name", width=200, anchor=tk.W)
        my_tree.column("Quantity", width=120, anchor=tk.W)

        # Create Headings
        my_tree.heading("Item Code", text='Item Code', anchor=tk.CENTER)
        my_tree.heading("Item Type", text='Item Type', anchor=tk.CENTER)
        my_tree.heading("Name", text='Name', anchor=tk.CENTER)
        my_tree.heading("Quantity", text='Quantity', anchor=tk.CENTER)

        # Display TreeView
        my_tree.pack()

        # configure scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Frame for upper buttons
        upperSide = tk.Frame(self)
        upperSide.grid(row=0, column=2, columnspan=4, sticky='e')

        # upperSide buttons
        men_btn = tk.Button(upperSide, text="Supplies", font=LARGE_FONT, command=lambda: controller.show_frame(Supplies))
        men_btn.grid(row=0, column=0, padx=10)

        his_btn = tk.Button(upperSide, text="Supplier", font=LARGE_FONT,
                            command=lambda: controller.show_frame(Supplier))
        his_btn.grid(row=0, column=1, padx=10)

        ord_btn = tk.Button(upperSide, text="Menu", font=LARGE_FONT, command=lambda: controller.show_frame(Menu))
        ord_btn.grid(row=0, column=2, padx=10)

        # Frame for Entries
        lowerSide = tk.Frame(self)
        lowerSide.grid(row=2, column=0, columnspan=6)

        # Labels and Entries for Lower Side
        icode = tk.Label(lowerSide, text="Item Code")
        icode.grid(row=0, column=0, padx=4)
        centry = tk.Entry(lowerSide, borderwidth=3)
        centry.grid(row=0,column=1, padx=4)

        itype = tk.Label(lowerSide, text="Item Type")
        itype.grid(row=0, column=2, padx=4)
        tentry = tk.Entry(lowerSide, borderwidth=3)
        tentry.grid(row=0, column=3, padx=4)

        iname = tk.Label(lowerSide, text="Item Name")
        iname.grid(row=1, column=0, padx=4)
        nentry = tk.Entry(lowerSide, borderwidth=3)
        nentry.grid(row=1, column=1, padx=4)

        qty = tk.Label(lowerSide, text="Item Quantity")
        qty.grid(row=1, column=2, padx=4)
        qty2 = tk.Entry(lowerSide, borderwidth=3)
        qty2.grid(row=1, column=3, padx=4)

        # buttons
        add = tk.Button(lowerSide, text="Add Item", font=LARGE_FONT, command=add)
        add.grid(row=2, column=0, padx=4, pady=5)
        modify = tk.Button(lowerSide, text="Update", font=LARGE_FONT, command=update)
        modify.grid(row=2, column=1, padx=4)
        delete = tk.Button(lowerSide, text="Delete Item", font=LARGE_FONT, command=delete)
        delete.grid(row=2, column=2, padx=4)
        clear = tk.Button(lowerSide, text="Clear", font=LARGE_FONT, command=clear)
        clear.grid(row=2, column=3, padx=4)

        displaydata()

        # Bindings
        # my_tree.bind("<ButtonRelease-1>", select_record)
        my_tree.bind("<ButtonRelease-1>", select_record)

class Menu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Menu", font=LARGE_FONT, bg="#98EFDA")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=40, sticky='w')

        tree_frame = tk.Frame(self)
        tree_frame.grid(row=1, column=1, columnspan=2, rowspan=4, pady=10, padx=10)

        # scroll
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Add TreeView
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, height=14)

        # Defining Columns
        my_tree['columns'] = ('CoffeeID', 'Coffee Type')

        # Formatting Column
        my_tree.column("#0", stretch=tk.NO, width=0)
        my_tree.column("CoffeeID", width=100, anchor=tk.W)
        my_tree.column("Coffee Type", width=150, anchor=tk.W)


        # Create Headings
        my_tree.heading("CoffeeID", text='CoffeeID', anchor=tk.CENTER)
        my_tree.heading("Coffee Type", text='Coffee Type', anchor=tk.CENTER)


        # Display TreeView
        my_tree.pack()

        # configure scrollbar
        tree_scroll.config(command=my_tree.yview)

        # --------------------------------------

        tree_frame2 = tk.Frame(self)
        tree_frame2.grid(row=2, column=4, columnspan=2, rowspan=3, pady=10, padx=10)

        comp = tk.Label(self, text="Coffee Component", font=LARGE_FONT, bg="#98EFDA" )
        comp.grid(row=1, column=4)

        # scroll
        tree_scroll2 = tk.Scrollbar(tree_frame2)
        tree_scroll2.pack(side=tk.RIGHT, fill=tk.Y)

        # Add TreeView
        my_tree2 = ttk.Treeview(tree_frame2, yscrollcommand=tree_scroll.set, height=12)

        # Defining Columns
        my_tree2['columns'] = ('Item Code', 'Item Name', 'Qty')

        # Formatting Column
        my_tree2.column("#0", stretch=tk.NO, width=0)
        my_tree2.column("Item Code", width=100, anchor=tk.W)
        my_tree2.column("Item Name", width=150, anchor=tk.W)
        my_tree2.column("Qty", width=100, anchor=tk.W)

        # Create Headings
        my_tree2.heading("Item Code", text='Item Code', anchor=tk.CENTER)
        my_tree2.heading("Item Name", text='Item Name', anchor=tk.CENTER)
        my_tree2.heading("Qty", text='Qty', anchor=tk.CENTER)

        # Display TreeView
        my_tree2.pack()

        # configure scrollbar
        tree_scroll2.config(command=my_tree2.yview)

        # Division TreeView
        def AddOrder():
            return

        def UpdateOrder():
            return

        def DeleteOrder():
            return

        # Frame for upper buttons
        upperSide = tk.Frame(self)
        upperSide.grid(row=0, column=2, columnspan=4, sticky='e')

        # upperSide buttons
        men_btn = tk.Button(upperSide, text="Supplies", font=LARGE_FONT, command=lambda: controller.show_frame(Supplies))
        men_btn.grid(row=0, column=1, padx=10)

        his_btn = tk.Button(upperSide, text="Supplier", font=LARGE_FONT,
                            command=lambda: controller.show_frame(Supplier))
        his_btn.grid(row=0, column=2, padx=10)

        inv_btn = tk.Button(upperSide, text="Inventory", font=LARGE_FONT, command=lambda: controller.show_frame(Inventory))
        inv_btn.grid(row=0, column=3, padx=10)

        # frame for bottom buttons
        bottomSide = tk.Frame(self)
        bottomSide.grid(row=5, column=0, columnspan=6)

        add_ord = tk.Button(bottomSide, text="Add Coffee", font=LARGE_FONT, command=AddOrder)
        add_ord.grid(row=0, column=0, padx=5)

        upd_ord = tk.Button(bottomSide, text="Update Coffee", font=LARGE_FONT, command=UpdateOrder)
        upd_ord.grid(row=0, column=1, padx=5)

        del_ord = tk.Button(bottomSide, text="Delete Coffee", font=LARGE_FONT, command=DeleteOrder)
        del_ord.grid(row=0, column=2, padx=5)

app = ImsCoffee()
app.geometry("720x440")
top = None
app.mainloop()

"""if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()"""