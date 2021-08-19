import tkinter as tk
from tkinter import *
from tkinter import ttk, END
# from PIL import ImageTk, Image
import sqlite3
from tkinter import messagebox

LARGE_FONT = ("Copperplate Gothic Bold", 12)


class ImsCoffee(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Menu, History, Inventory, Order):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Menu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Menu(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Menu", font=LARGE_FONT, bg = "#98EFDA")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=50, sticky='w')

        """button = tk.Button(self, text="Visit Page 1",
                           command=lambda: controller.show_frame(PageOne))
        button.grid(row=2, column=0,)

        button2 = tk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.grid(row=3, column=0,)"""
        def dbSetup():
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

        def addProduct():


            return

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
        tree_frame.grid(row=1, column=3, columnspan=3, pady=10)

        # scroll
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Add TreeView
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, height=16)

        # Defining Columns
        my_tree['columns'] = ('CoffeeID', 'Type', 'Quantity')

        # Formatting Column
        my_tree.column("#0", stretch=tk.NO, width=0)
        my_tree.column("CoffeeID", width=150, anchor=tk.W)
        my_tree.column("Type", width=200, anchor=tk.W)
        my_tree.column("Quantity", width=150, anchor=tk.W)

        # Create Headings
        my_tree.heading("CoffeeID", text='CoffeeID', anchor=tk.CENTER)
        my_tree.heading("Type", text='Type', anchor=tk.CENTER)
        my_tree.heading("Quantity", text='Quantity', anchor=tk.CENTER)

        # Display TreeView
        my_tree.pack()

        # configure scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Frame for left buttons
        leftSide = tk.Frame(self)
        leftSide.grid(row=1, column=0, columnspan=2)
        
        # Frame for upper buttons
        upperSide = tk.Frame(self)
        upperSide.grid(row=0, column=2, columnspan=4, sticky='e')

        # LeftSide Buttons
        add_btn = tk.Button(leftSide, text="Add product", font=LARGE_FONT, command=addProduct)
        add_btn.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        del_btn = tk.Button(leftSide, text="Delete product", font=LARGE_FONT)
        del_btn.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        log_btn = tk.Button(leftSide, text="Sign out", font=LARGE_FONT)
        log_btn.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

        # upperSide buttons
        his_btn = tk.Button(upperSide, text="History", font=LARGE_FONT, command=lambda: controller.show_frame(History))
        his_btn.grid(row=0, column=0, padx=10)

        inv_btn = tk.Button(upperSide, text="Inventory", font=LARGE_FONT,
                            command=lambda: controller.show_frame(Inventory))
        inv_btn.grid(row=0, column=1, padx=10)

        ord_btn = tk.Button(upperSide, text="Order", font=LARGE_FONT, command=lambda: controller.show_frame(Order))
        ord_btn.grid(row=0, column=2, padx=10)


class History(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="History", font=LARGE_FONT, bg="#98EFDA")
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
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, height=16)

        # Defining Columns
        my_tree['columns'] = ('Transaction ID', 'Order', 'Size', 'Quantity', 'Date', 'Time')

        # Formatting Column
        my_tree.column("#0", stretch=tk.NO, width=0)
        my_tree.column("Transaction ID", width=100, anchor=tk.W)
        my_tree.column("Order", width=150, anchor=tk.W)
        my_tree.column("Size", width=60, anchor=tk.W)
        my_tree.column("Quantity", width=80, anchor=tk.W)
        my_tree.column("Date", width=140, anchor=tk.W)
        my_tree.column("Time", width=120, anchor=tk.W)

        # Create Headings
        my_tree.heading("Transaction ID", text='TransactionID', anchor=tk.CENTER)
        my_tree.heading("Order", text='Order', anchor=tk.CENTER)
        my_tree.heading("Size", text='Size', anchor=tk.CENTER)
        my_tree.heading("Quantity", text='Quantity', anchor=tk.CENTER)
        my_tree.heading("Date", text='Date', anchor=tk.CENTER)
        my_tree.heading("Time", text='Time', anchor=tk.CENTER)

        # Display TreeView
        my_tree.pack()

        # configure scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Frame for upper buttons
        upperSide = tk.Frame(self)
        upperSide.grid(row=0, column=2, columnspan=4, sticky='e')

        # upperSide buttons
        men_btn = tk.Button(upperSide, text="Menu", font=LARGE_FONT, command=lambda: controller.show_frame(Menu))
        men_btn.grid(row=0, column=0, padx=10)

        inv_btn = tk.Button(upperSide, text="Inventory", font=LARGE_FONT,
                            command=lambda: controller.show_frame(Inventory))
        inv_btn.grid(row=0, column=1, padx=10)

        ord_btn = tk.Button(upperSide, text="Order", font=LARGE_FONT, command=lambda: controller.show_frame(Order))
        ord_btn.grid(row=0, column=2, padx=10)


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
                    item_type TEXT,
                    item_name TEXT NOT NULL,
                    quantity INT,
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
                "UPDATE Inventory set  item_code=?, item_type=?, item_name=?, quantity=?,  WHERE item_code=?",
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
        men_btn = tk.Button(upperSide, text="Menu", font=LARGE_FONT, command=lambda: controller.show_frame(Menu))
        men_btn.grid(row=0, column=0, padx=10)

        his_btn = tk.Button(upperSide, text="History", font=LARGE_FONT,
                            command=lambda: controller.show_frame(History))
        his_btn.grid(row=0, column=1, padx=10)

        ord_btn = tk.Button(upperSide, text="Order", font=LARGE_FONT, command=lambda: controller.show_frame(Order))
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

class Order(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Order", font=LARGE_FONT, bg="#98EFDA")
        label.grid(row=0, column=0, columnspan=2, pady=10, padx=40, sticky='w')

        tree_frame = tk.Frame(self)
        tree_frame.grid(row=1, column=1, columnspan=2, rowspan=4, pady=10, padx=10)

        # scroll
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Add TreeView
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, height=14)

        # Defining Columns
        my_tree['columns'] = ('Order No.', 'Time', 'Date')

        # Formatting Column
        my_tree.column("#0", stretch=tk.NO, width=0)
        my_tree.column("Order No.", width=125, anchor=tk.W)
        my_tree.column("Time", width=100, anchor=tk.W)
        my_tree.column("Date", width=100, anchor=tk.W)

        # Create Headings
        my_tree.heading("Order No.", text='Order No.', anchor=tk.CENTER)
        my_tree.heading("Time", text='Time', anchor=tk.CENTER)
        my_tree.heading("Date", text='Date', anchor=tk.CENTER)

        # Display TreeView
        my_tree.pack()

        # configure scrollbar
        tree_scroll.config(command=my_tree.yview)

        # --------------------------------------

        tree_frame2 = tk.Frame(self)
        tree_frame2.grid(row=2, column=4, columnspan=2, rowspan=3, pady=10, padx=10)

        comp = tk.Label(self, text="Order Component", font=LARGE_FONT, bg="#98EFDA" )
        comp.grid(row=1, column=4)

        # scroll
        tree_scroll2 = tk.Scrollbar(tree_frame2)
        tree_scroll2.pack(side=tk.RIGHT, fill=tk.Y)

        # Add TreeView
        my_tree2 = ttk.Treeview(tree_frame2, yscrollcommand=tree_scroll.set, height=12)

        # Defining Columns
        my_tree2['columns'] = ('Coffee Name', 'Size', 'Qty')

        # Formatting Column
        my_tree2.column("#0", stretch=tk.NO, width=0)
        my_tree2.column("Coffee Name", width=125, anchor=tk.W)
        my_tree2.column("Size", width=75, anchor=tk.W)
        my_tree2.column("Qty", width=100, anchor=tk.W)

        # Create Headings
        my_tree2.heading("Coffee Name", text='Order No.', anchor=tk.CENTER)
        my_tree2.heading("Size", text='Time', anchor=tk.CENTER)
        my_tree2.heading("Qty", text='Date', anchor=tk.CENTER)

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
        men_btn = tk.Button(upperSide, text="Menu", font=LARGE_FONT, command=lambda: controller.show_frame(Menu))
        men_btn.grid(row=0, column=1, padx=10)

        his_btn = tk.Button(upperSide, text="History", font=LARGE_FONT,
                            command=lambda: controller.show_frame(History))
        his_btn.grid(row=0, column=2, padx=10)

        inv_btn = tk.Button(upperSide, text="Inventory", font=LARGE_FONT, command=lambda: controller.show_frame(Inventory))
        inv_btn.grid(row=0, column=3, padx=10)

        # frame for bottom buttons
        bottomSide = tk.Frame(self)
        bottomSide.grid(row=5, column=0, columnspan=6)

        add_ord = tk.Button(bottomSide, text="Add Order", font=LARGE_FONT, command=AddOrder)
        add_ord.grid(row=0, column=0, padx=5)

        upd_ord = tk.Button(bottomSide, text="Update Order", font=LARGE_FONT, command=UpdateOrder)
        upd_ord.grid(row=0, column=1, padx=5)

        del_ord = tk.Button(bottomSide, text="Delete Order", font=LARGE_FONT, command=DeleteOrder)
        del_ord.grid(row=0, column=2, padx=5)

app = ImsCoffee()
app.geometry("720x440")
app.mainloop()

"""if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()"""