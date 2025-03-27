import tkinter
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as SQL


def main_gui():
    window = tkinter.Tk()
    window.title("Data Entery Form")

    frame = tkinter.Frame(window)
    frame.pack()

    def enter_data():
        accepted = accept_var.get()

        if accepted == "Accepted":

        # User info
            firstname = first_name_entry.get()
            lastname = last_name_entry.get()

            if firstname and lastname:
                title = title_combobox.get()
                if age_spinbox.get() == int:
                    age = age_spinbox.get()
                else:
                    tkinter.messagebox.showwarning(title="ERROR", message="Age must be integer")
                nationality = nationality_combobox.get()

                # Couse Info
                registration_status = reg_status_var.get()
                numcouses = numcouses_spinbox.get()
                numsemester = numsemester_Spinbox.get()

                print(f"{firstname}, {lastname}, {title}, {age}, {nationality}, {registration_status}, {numcouses}, {numsemester}")
            
                conn = SQL.connect('student_data.db')
                
                table_create_query = '''
                    CREATE TABLE IF NOT EXISTS Student_data
                    (firstname TEXT, lastname TEXT, title TEXT, age INT, nationality TEXT,
                    registration_status TEXT, num_couses INT, num_semesters INT)
                    '''
                conn.execute(table_create_query)

                data_insert_query = '''
                    INSERT INTO Student_data
                    (firstname, lastname, title, age, nationality, registration_status, num_couses, num_semesters)
                    VALUES (?, ?, ?, ? , ?, ?, ?, ?)
                    '''
                data_insert_tuple = (firstname, lastname, title, age, nationality, registration_status, numcouses, numsemester)

                cur = conn.cursor()
                cur.execute(data_insert_query, data_insert_tuple)
                conn.commit()
                conn.close()
            
            else:
                tkinter.messagebox.showwarning(title="ERROR", message="Fist and Last name are required")
        else:
            tkinter.messagebox.showwarning(title="ERROR", message="You have not accepted the terms")

    # Saving user info
    user_info_frame = tkinter.LabelFrame(frame, text="User Information")
    user_info_frame.grid(row=0, column=0, padx=20, pady=10)

    first_name_label = tkinter.Label(user_info_frame, text="First Name")
    first_name_label.grid(row=0, column=0)
    last_name_label = tkinter.Label(user_info_frame, text="Last Name")
    last_name_label.grid(row=0, column=1)

    first_name_entry = tkinter.Entry(user_info_frame)
    last_name_entry = tkinter.Entry(user_info_frame)
    first_name_entry.grid(row=1, column=0)
    last_name_entry.grid(row=1, column=1)

    title_lable = tkinter.Label(user_info_frame, text="Title")
    title_combobox = ttk.Combobox(user_info_frame, values=["", "Mr.", "Ms.", "Dr."])
    title_lable.grid(row=0, column=2)
    title_combobox.grid(row=1, column=2)

    age_label = tkinter.Label(user_info_frame, text="Age")
    age_spinbox = tkinter.Spinbox(user_info_frame, from_=10, to=110)
    age_label.grid(row=2, column=0)
    age_spinbox.grid(row=3, column=0)

    nationality_label = tkinter.Label(user_info_frame, text="Nationality")
    nationality_combobox = ttk.Combobox(user_info_frame, values=["Afica", "Europe", "America", "Asia"])
    nationality_label.grid(row=2, column=1)
    nationality_combobox.grid(row=3, column=1)

    for widget in user_info_frame.winfo_children():
        widget.grid_configure(padx=10, pady=10)

    # Saving Course Info
    courses_frame = tkinter.LabelFrame(frame)
    courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

    registrated_label = tkinter.Label(courses_frame, text="Registration Status")

    reg_status_var = tkinter.StringVar(value="Not Registered")
    registrated_check = tkinter.Checkbutton(courses_frame, text="Currently Registered", 
                                            variable=reg_status_var, onvalue="Registered", offvalue="Not Registered")

    registrated_label.grid(row=0, column=0)
    registrated_check.grid(row=1, column=0)

    numcouses_lable = tkinter.Label(courses_frame, text="# Completed Couses")
    numcouses_spinbox = tkinter.Spinbox(courses_frame, from_=0, to='infinity')
    numcouses_lable.grid(row=0, column=1)
    numcouses_spinbox.grid(row=1, column=1)

    numsemester_label = tkinter.Label(courses_frame, text="# Semesters")
    numsemester_Spinbox = tkinter.Spinbox(courses_frame, from_=0, to='infinity')
    numsemester_label.grid(row=0, column=2)
    numsemester_Spinbox.grid(row=1, column=2)

    for widget in courses_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    # Accept terms
    terms_frame = tkinter.LabelFrame(frame, text="Terms & Conditions")
    terms_frame.grid(row=2, column=0, sticky='news', padx=20, pady=10)

    accept_var = tkinter.StringVar(value="Not Accepted")
    terms_check = tkinter.Checkbutton(terms_frame, text="I accept the terms and conditions",
                                    variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
    terms_check.grid(row=0, column=0)

    # Button
    button = tkinter.Button(frame, text="Enter data", command= enter_data)
    button.grid(row=3, column=0, sticky='new', padx=20, pady=10)

    window.mainloop()


def second_gui():

    def insert_data():
        voornaam = first_name_entry.get()
        achternaam = last_name_entry.get()
        gayness = gayness_entry.get()
        IQ_level = IQ_level_combobox.get()

        conn = SQL.connect('gang_levels.db')
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS gang_levels
        (Voornaam TEXT, Achternaam TEXT, Gayness INT, IQ TEXT)
        '''
        conn.execute(create_table_query)
        cur = conn.cursor()
        insert_query = '''
        INSERT INTO gang_levels
        VALUES (?, ?, ?, ?)            
        '''
        entry_tupel = (voornaam, achternaam, gayness, IQ_level)
        cur.execute(insert_query, entry_tupel)
        conn.commit()
        conn.close()

        print(voornaam, achternaam, gayness, IQ_level)

    window = tkinter.Tk()
    window.title("Gang form")

    frame = tkinter.Frame(window)
    frame.pack()

    main_info_frame = tkinter.LabelFrame(frame, text="Main info")
    main_info_frame.grid(row=0, column=0, padx=20, pady=20)

    first_name_label = tkinter.Label(main_info_frame, text="Voornaam")
    first_name_label.grid(row=0, column=0)
    last_name_label = tkinter.Label(main_info_frame, text="Achternaam")
    last_name_label.grid(row=0, column=1)

    first_name_entry = tkinter.Entry(main_info_frame)
    first_name_entry.grid(row=1, column=0)
    last_name_entry = tkinter.Entry(main_info_frame)
    last_name_entry.grid(row=1, column=1)

    for widget in main_info_frame.winfo_children():
        widget.grid_configure(padx=10, pady=10)

    secondary_info_frame = tkinter.LabelFrame(frame, text="Belangrijke info")
    secondary_info_frame.grid(row=1, column=0, padx=20, pady=20)

    gayness_label = tkinter.Label(secondary_info_frame, text="Enter gayness level")
    gayness_label.grid(row=0, column=0)
    gayness_entry = tkinter.Spinbox(secondary_info_frame, from_=800, to='infinity')
    gayness_entry.grid(row=1, column=0)

    IQ_level_label = tkinter.Label(secondary_info_frame, text="IQ level")
    IQ_level_label.grid(row=0, column=1)
    IQ_level_combobox = ttk.Combobox(secondary_info_frame, values=['Non-existent', '90', '+9000'])
    IQ_level_combobox.grid(row=1, column=1)

    third_frame = tkinter.LabelFrame(frame, text='Belangrijkste info')
    third_frame.grid(row=2, column=0)

    nigger_hate = tkinter.Label(third_frame, text="Eet jij sushi??")
    nigger_hate.grid(row=0, column=0, pady=10)
    nigger_hate_combobox = ttk.Combobox(third_frame, values=['Ja', 'Jaaa', 'Fok die sushi'])
    nigger_hate_combobox.grid(row=1, column=0)

    for widget in secondary_info_frame.winfo_children():
        widget.grid_configure(padx=10, pady=10)

    button = tkinter.Button(frame, text="Enter data", command= insert_data)
    button.grid(row=3, column=0, pady= 20)

    window.mainloop()


second_gui()