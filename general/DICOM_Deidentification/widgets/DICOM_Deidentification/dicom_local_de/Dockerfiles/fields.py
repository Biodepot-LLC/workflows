import sys
import copy
from tkinter import Tk, Frame, Checkbutton, Scrollbar, Canvas, messagebox, BooleanVar
from tkinter.constants import BOTH, Y, LEFT

class DICOMDeidentifier(Frame):
    def __init__(self, parent, dicom_fields_file):
        Frame.__init__(self, parent)
        self.dicom_fields_file = dicom_fields_file
        self.checkboxes = []
        self.checkbox_attributes = []
        self.buttons = []
        self.parent = parent
        self.setup_components()

    def setup_components(self):
        self.pack(fill=BOTH, expand=1)
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

        sel = read_selected_dicom_fields(self.dicom_fields_file)
        data = read_dicom_field_json_file('list.json')
        load_checkboxes_on_canvas(self, data, copy.deepcopy(sel))
        
    def on_closing(self):
        import os
        selected_list = []
        saved_file = os.path.dirname(os.path.abspath('list.txt'))
        if messagebox.askokcancel("Exit", "Would you like to quit? (DICOM fields selected will be save in {})".format(saved_file)):
            for cb_att in self.checkbox_attributes:
                cb_val, cb_tag = cb_att
                if cb_val.get():
                    selected_list.append(cb_tag)
            write_selected_dicom_fields(self.dicom_fields_file, ",".join(selected_list))
            self.parent.destroy()

def read_dicom_field_json_file(file_path):
    import json
    data = None
    try:
        reader = open(file_path)
        data = json.loads(reader.readline())
    finally:
        reader.close()
        return data

def read_selected_dicom_fields(file_path):
    data = None
    try:
        reader = open(file_path)
        data = reader.readline().split(',')
    except FileNotFoundError:
        with open(file_path, 'w'):
            pass
        reader = open(file_path)
        data = reader.readline().split(',')
    finally:
        reader.close()
        return data

def write_selected_dicom_fields(file_path, data):
    try:
        writer = open(file_path, "w")
        writer.write(data)
    finally:
        writer.close()

def load_checkboxes_on_canvas(parent, data, selected_list):
    
    rows = 0
    columns = 2
    x = 0
    
    size = len(data)
    #selected_list.sort()
    try:
        while x < size:
            count = 0
            while count < columns:
                b = BooleanVar()
                l = Checkbutton(parent, text=data[x]["attribute_name"], variable=b)
                l.grid(row=rows, column=count, sticky='w')
                
                parent.checkboxes.append(l)
                parent.checkbox_attributes.append([b, data[x]['attribute_id']])
                
                if len(selected_list) > 0 and selected_list[0] == data[x]['attribute_id']:
                    l.select()
                    selected_list.pop(0)
                count = count + 1
                x = x + 1
            rows = rows + 1
    except IndexError:
        print("Could not find {} in the list".format(selected_list))

def main():
    args = sys.argv
    dicom_fields_file = 'list.txt' 
    if len(args) > 1:
        dicom_fields_file = args[1]

    r = Tk()
    r.title("Excluded DICOM Fields")
    s = Scrollbar(r)
    c = Canvas(r, background = "#d2d2d2", yscrollcommand=s.set)
    f = DICOMDeidentifier(r, dicom_fields_file)
    s.config(command=c.yview)
    s.pack(side=LEFT, fill=Y) 
    c.pack(side="left", fill="both", expand=True)
    c.create_window(0, 0, window=f, anchor='nw')
    r.update()
    
    # r.geometry('600x700+200+100')
    r.minsize(750, 500)
    r.maxsize(750, 500)
    r.mainloop()

if __name__ == '__main__':
    main()
