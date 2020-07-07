# Student Name : LIMBA GEORGE CRISTIAN
# Email Adress : cristi201199@gmail.com
# Phone Number : 0894757956 

import tkinter as tk
from tkinter import ttk, Text
import re
from datetime import datetime

class BMI (ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding ="10 10 10 10")
        self.grid(column=0, row=0, sticky="ew")
        
        #Define variabels for text entry fields
        self.user_name=tk.StringVar()
        self.user_height=tk.StringVar()
        self.user_height_imp=tk.StringVar()
        self.user_weight= tk.StringVar()
        self.user_weight_imp=tk.StringVar()
        self.BMI=tk.StringVar()
        self.BMI_display=tk.StringVar()
        self.unit = tk.IntVar()
        self.unit.set(1)
        self.display_buttons()
        self.clear_button()
        
        #Radio button value
    def change_unit(self, unit):
        self.unit = unit
    
    def display_buttons(self):
        but1=ttk.Radiobutton(self, text='Metric', value=1, command=self.change_unit_clear, variable=self.unit).grid(row=0, column=0, sticky="ew")
        but2=ttk.Radiobutton(self, text='Imperial', value=2, command=self.change_unit_clear,  variable=self.unit).grid(row=0, column=1, sticky="ew")
        ttk.Label(self, text="Name").grid(row=2, sticky="ew")
        ttk.Entry(self, width=30, textvariable = self.user_name).grid(row=3, columnspan=2, sticky="ew")
        ttk.Label(self, text="Height", font=("Verdana 10 underline")).grid(row=4, sticky="ew")
        self.height_label = ttk.Label(self, text="Cm")
        self.height_label.grid(row=5, columnspan=2, sticky="ew")
        self.height_entry=ttk.Entry(self, textvariable= self.user_height)
        self.height_entry.grid(column=0, columnspan=2, row=6, sticky="ew")
        ttk.Label(self, text= "Weight", font=("Verdana 10 underline")).grid(sticky="ew", row=7)
        self.weight_label = ttk.Label(self, text="Kg")
        self.weight_label.grid(row=8, columnspan=2, sticky="ew")
        self.weight_entry=ttk.Entry(self, textvariable=self.user_weight)
        self.weight_entry.grid(column=0, columnspan=2, row=9, sticky="ew")
        ttk.Label(self, text="Body Mass Index").grid(row=10, columnspan=2, sticky="ew")
        ttk.Entry(self, width=30, textvariable=self.BMI, state="readonly").grid(row=11, columnspan=2, sticky="ew")
        self.text_box = Text(self, width=30, height=5, state=tk.DISABLED)
        self.text_box.grid(row=12, columnspan=2, sticky="ew")
        self.text_box.tag_config("red", foreground="red", background="black")
        self.text_box.tag_config("yellow", foreground="yellow", background='black')
        self.text_box.tag_config("green", foreground="green", background="black")
        ttk.Button(self, text="Calculate", command=self.calculate).grid(row=13, sticky="ew", columnspan=2)
        ttk.Button(self, text="Clear", command=self.clear_button).grid(row=14, sticky="ew", columnspan=2)
    
    # Special config for imperial
    def display_imperial_units(self):
        self.weight_label.config(text="Stones")
        self.height_label.config(text="Feet")
        self.height_label_imp = ttk.Label(self, text="Inchies")
        self.height_label_imp.grid(column=1, row=5, sticky="ew")
        self.height_entry_imp=ttk.Entry(self, textvariable=self.user_height_imp)
        self.height_entry_imp.grid(column=1, row=6, columnspan=2, sticky="ew")
        self.weight_label_imp = ttk.Label(self, text="Pounds")
        self.weight_label_imp.grid(column=1, row=8, sticky="ew")
        self.weight_entry_imp=ttk.Entry(self,textvariable=self.user_weight_imp)
        self.weight_entry_imp.grid(column=1, row=9, columnspan=2, sticky="ew")

       #Special config for metric
    def display_metric_units(self):
        self.weight_label.config(text="Kg")
        self.height_label.config(text="Cm")
        self.height_entry_imp.destroy()
        self.weight_entry_imp.destroy()
        self.height_label_imp.destroy()
        self.weight_label_imp.destroy()

        #Clear input if you change method by radio button
    def change_unit_clear(self):
        self.user_height.set("")
        self.user_weight.set("")
        self.BMI.set("")
        self.write_text_box("")
        self.user_height_imp.set("")
        self.user_weight_imp.set("")
        if self.unit.get() == 1:
            self.display_metric_units()
        else:
            self.display_imperial_units()

        #Config text_box
    def write_text_box(self, text, tag = 'green'):
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(1.0, text, tag)
        self.text_box.config(state=tk.DISABLED)

    
    def calculate(self):
        self.BMI.set("")
        self.write_text_box("")
        
        # exception handling
        try:
            user_name = self.user_name.get()
            if(bool(re.match(r".*\d+.*", user_name))):
                raise ValueError("Invalid Name")

            if self.unit.get() == 1:
                user_height=float(self.user_height.get())
                user_weight= float(self.user_weight.get())
                if(user_height < 0 or user_weight < 0):
                     raise Exception("Invalid Height or weight")

                bmi = self.metric(user_weight, user_height)
                weight_unit = 'kg'
                self.csv_file(user_name, user_height, user_weight)
            else:
                user_height = float(self.user_height.get())
                user_weight = float(self.user_weight.get())
                user_height_imp = float(self.user_height_imp.get())
                user_weight_imp = float(self.user_weight_imp.get())
                 
                if(user_height < 0 or user_weight < 0):
                     raise Exception("Invalid Height or weight")

                bmi = self.imperial(user_weight, user_height, user_height_imp, user_weight_imp)
                weight_unit = 'pounds'
                self.csv_file(user_name, user_height, user_weight, user_height_imp, user_weight_imp)

            self.display_bmi(bmi, user_name, weight_unit)
            
        except: 
            self.write_text_box("Invalid input", 'red')
       
        # Display information for uset in text_box
    def display_bmi(self, bmi, user_name, weight_unit):
        self.BMI.set(bmi)

        if (bmi < 18.5):
            self.write_text_box("%s your %s are %.2f. \n Conform BMI you are Under Weigth" % (user_name, weight_unit, bmi), "red")
        elif(18.5 < bmi < 24.9):
            self.write_text_box("%s your %s are %.2f. \n Conform BMI you are Heathy Weight" % (user_name, weight_unit, bmi), "green")
        elif(24.9 < bmi < 29.9):
            self.write_text_box("%s your %s are %.2f. \n Conform BMI you are Overweight" % (user_name, weight_unit, bmi), "yellow")
        else:
            self.write_text_box("%s your %s are %.2f. \n Conform BMI you are Obese" % (user_name, weight_unit, bmi), "red")
       
     # Metric BMI Formula
    def metric(self, user_weight, user_height):
        return round(user_weight / ((user_height / 100) ** 2) , 2)
        
     # English Imperial BMI Formula
    def imperial(self, user_weight, user_height, user_height_imp, user_weight_imp):
        user_height = float(user_height * 12)
        user_weight = float(user_weight *14)
        final_mass = user_weight + user_weight_imp
        final_height= user_height +user_height_imp

        return round(( 703 * final_mass) / (final_height ** 2), 2)

    # Create Csv file  and check the rigth method
    
    def csv_file(self, user_name, user_height, user_weight = None, user_height_imp = None, user_weight_imp = None):
        current_date_time = datetime.now()
        date_time = current_date_time.strftime("%d/%m/%Y %H:%M:%S")
        if self.unit.get() == 1:
            file = open("BMI.csv", "a", newline="")
            input_user = f'{user_name}, {user_height}, {user_weight}, {date_time}\n'
            csv=file.write(input_user) # Loop in tupels because file.write take just 1 argumet 
            csv_close=file.close()
        else: 
            user_height= float(user_height * 12)
            user_weight=float(user_weight *14)
            final_mass = user_weight + user_weight_imp
            final_height= user_height + user_height_imp
            file= open("BMI.csv", "a", newline="")
            input_user=(user_name,"," , final_height,",", final_mass, ",", date_time, "\n")
            for f in input_user:
                csv=file.write(str(f))  # Loop in tupels because file.write take just 1 argumet
            csv_close=file.close()
    
    
    #Command for clear button
    def clear_button(self):
        self.user_name.set("")
        self.user_height.set("")
        self.user_weight.set("")
        self.BMI.set("")
        self.write_text_box("")
        self.user_height_imp.set("")
        self.user_weight_imp.set("")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Body Mass Index")
    root.iconbitmap("icon.ico")
    BMI(root)
    root.mainloop()
