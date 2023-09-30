from tkinter import Text,Entry
from tabulate import tabulate
import mysql.connector
from customtkinter import CTk,CTkLabel,CTkButton,CTkFrame,CTkScrollableFrame,CTkEntry,StringVar,BOTTOM,RIGHT,TOP,LEFT,END,set_appearance_mode,set_default_color_theme,CTkTabview
from pickle import load,dump
import os


app=CTk()
set_appearance_mode("dark")
set_default_color_theme("blue")
app.geometry("600x250")
app.title("MYSQL~EDITOR")
app.resizable(False,False)
Connection=None

def session_manager(button):
    global dictionary_session_buttons,current_button
    def event_handler(event):
        for child in Login_frame.winfo_children():
            child.configure(state="normal")
        try:
            host.delete("0",END)
            user.delete("0",END)
            password.delete("0",END)
        except:
            pass
        global current_button
        for i in dictionary_session_buttons.values():
            i.configure(fg_color="transparent")

        button.configure(fg_color="red")

        current_button=[button.cget("text")]

        with open(r"D:\GOKUL PERSONAL\python prog\MYSQL EDITOR-SELF\mysql~editor session.dat","rb") as file:
            list_data_temp=[]
            try:
                while True:
                    list_data_temp.append(load(file))
            except:
                pass
            for i in list_data_temp:
                for j in i:
                    if j[0]+str(j[1])==current_button[0]:
                        if i[j]==[]:
                            break
                        else:
                            host.insert("0",i[j][0])
                            user.insert("0",i[j][1])
                            password.insert("0",i[j][2])
                            break

    return event_handler

def session_creation():
    global session_list, dictionary_session_buttons
    with open(r"D:\GOKUL PERSONAL\python prog\MYSQL EDITOR-SELF\mysql~editor session.dat", "ab+") as file:
        if session_list!=[]:
            dump({("session-",list(session_list[-1].keys())[0][1]+1):[]},file)
            dictionary_session_buttons[f"session-{list(session_list[-1].keys())[0][1]+1}"] = CTkButton(session_frame, text=f"session-{list(session_list[-1].keys())[0][1]+1}",fg_color="transparent",hover_color="red")
            dictionary_session_buttons[f"session-{list(session_list[-1].keys())[0][1]+1}"].pack()
        else:
            dump({("session-", 1): []}, file)
            dictionary_session_buttons["session-1"]=CTkButton(session_frame,text="session-1",fg_color="transparent",hover_color="red")
            dictionary_session_buttons["session-1"].pack()
        file.seek(0)
        try:
            while True:
                lst = load(file)
        except:
            pass
        session_list.append(lst)

        if session_list != []:
            pass

def connect():
        global Connection
        try:
            host_get=host.get()
            user_get=user.get()
            password_get=password.get()
            Connection=mysql.connector.connect(
                host=f"{host_get}",
                user=f"{user_get}",
                password=f"{password_get}")
            file1=open(r"D:\GOKUL PERSONAL\python prog\MYSQL EDITOR-SELF\temp.dat","wb")
            with open(r"D:\GOKUL PERSONAL\python prog\MYSQL EDITOR-SELF\mysql~editor session.dat","rb") as file:
                list_data=[]
                try:
                    while True:
                        list_data.append(load(file))
                except EOFError:
                    pass

                for i in list_data:
                    for j in i:
                        if current_button[0]==j[0]+str(j[1]):
                            i[j]=[host_get,user_get,password_get]
                            for i in list_data:
                                dump(i,file1)
                            flag=True
                            break
                        else:
                            flag=False
                    if flag==True:
                        break
            file1.close()
            os.remove("D:\GOKUL PERSONAL\python prog\MYSQL EDITOR-SELF\mysql~editor session.dat")
            os.rename(r"D:\GOKUL PERSONAL\python prog\MYSQL EDITOR-SELF\temp.dat",
                      r"D:\GOKUL PERSONAL\python prog\MYSQL EDITOR-SELF\mysql~editor session.dat")

            Login_frame.destroy()
            session_frame.destroy()
            __main__()
        except :
            CTkLabel(Login_frame,text="Wrong Credentials").place(x=150,y=200)

def connect_to_mysql():
    global Login_frame,session_frame,host,user,password
    Login_frame=CTkFrame(app,height=600,width=400)
    Login_frame.place(x=0,y=0)

    session_frame=CTkScrollableFrame(app,height=600,width=200)
    session_frame.place(x=403,y=0)
    
    CTkLabel(Login_frame,text="Enter host id / name").place(x=0,y=1)
    host=CTkEntry(Login_frame)
    host.place(x=150,y=1)

    CTkLabel(Login_frame,text="Enter user id").place(x=0,y=50)
    user=CTkEntry(Login_frame)
    user.place(x=150,y=50)

    CTkLabel(Login_frame,text="Enter Password").place(x=0,y=100)
    password=CTkEntry(Login_frame)
    password.place(x=150,y=100)



    Create_session=CTkButton(session_frame,text="Create new Session",fg_color="transparent",anchor="center",hover_color="red",command=session_creation)
    Create_session.pack()

    
    submit=CTkButton(Login_frame,text="Submit",command=connect)
    submit.place(x=150,y=150)

def TableSelection(button):
    def event_handler_TableSelection(event):
        try:
            for widgets in desc_frame.winfo_children():
                widgets.destroy()

            for widgets in Data_frame.winfo_children():
                widgets.destroy()
        except:
            pass
        for child in list_of_table_frame.winfo_children():
            child.configure(fg_color="transparent")
        button.configure(fg_color="red")
        desc_label_table.configure(text=f"DESC TABLE:- {button.cget('text')}")
        data_label.configure(text=f"DATA FROM TABLE:- {button.cget('text')}")

        Cursor.execute(f"DESC `{button.cget('text')}`;")
        heading=[i[0] for i in Cursor.description]
        dict_heading={}
        for i in range(len(heading)):
            dict_heading[heading[i]]=Entry(desc_frame,bg="#333333",foreground="white")
            dict_heading[heading[i]].insert("0",heading[i])
            dict_heading[heading[i]].grid(row=0,column=i+1)

        list_desc_table=[i for i in Cursor.fetchall()]
        dict_table_desc={}
        row_count,column_count=2,1
        for i in  list_desc_table:
            for j in i:
                j=str(j)
                dict_table_desc[j]=Entry(desc_frame,bg="#333333",foreground="white")
                dict_table_desc[j].insert("0",j)
                dict_table_desc[j].grid(row=row_count,column=column_count)
                column_count+=1
            row_count+=1
            column_count=1

        Cursor.execute(f"SELECT * FROM `{button.cget('text')}`;")

        list_headers_data=[i[0] for i in Cursor.description]
        dict_headers_data={}
        for i in range(len(list_headers_data)):
            dict_headers_data[list_headers_data[i]]=Entry(Data_frame,bg="#333333",foreground="white")
            dict_headers_data[list_headers_data[i]].insert("0",list_headers_data[i])
            dict_headers_data[list_headers_data[i]].grid(row=0,column=i+1)
        list_data_of_currentTable=[i for i in Cursor.fetchall()]
        dict_data_of_currentTable={}
        row_count, column_count = 2, 1
        for i in list_data_of_currentTable:
            for j in i:
                j=str(j)
                dict_data_of_currentTable[j]=Entry(Data_frame,bg="#333333",foreground="white")
                dict_data_of_currentTable[j].insert("0",j)
                dict_data_of_currentTable[j].grid(row=row_count,column=column_count)
                column_count+=1
            row_count+=1
            column_count=1

    return event_handler_TableSelection
def Database_selection(button):
    global dict_list_of_tables_button
    def database_eventhandler(event):
        global dict_list_of_tables_button
        label_table_database_inuse.configure(text=f"TABLES FROM :-{button.cget('text')}")
        try:
            for child in list_of_table_frame.winfo_children():
                child.destroy()
        except:
            pass
        for others in dictionary_databases:
            dictionary_databases[others].configure(fg_color="transparent")
        button.configure(fg_color="red")
        Cursor.execute(f"USE `{button.cget('text')}`;")
        Cursor.execute("SHOW TABLES;")

        list_of_tables=[i[0] for i in Cursor.fetchall()]

        dict_list_of_tables_button={i:CTkButton(list_of_table_frame,text=i,fg_color="transparent",anchor="w",hover_color="red") for i in list_of_tables}

        row_count=0
        for i in dict_list_of_tables_button:
            table_handler=TableSelection(dict_list_of_tables_button[i])
            dict_list_of_tables_button[i].bind("<Button-1>",table_handler)
            dict_list_of_tables_button[i].grid(row=row_count,column=0)
            row_count+=1

    return database_eventhandler
def Query_mode():
    query_app=CTk()
    query_app.state("zoomed")
    query_app.title("Query Window")

    query_frame=CTkScrollableFrame(query_app,height=350,width=1350)
    query_frame.place(x=0,y=30)

    def Run_query():
        try:
            for i in Output_frame.winfo_children():
                i.destroy()
        except:
            pass
            
        query=Query_text.get("0.0",END)
        query_list=[]
        flag=False
        query_appening=""
        for i in query:
            if i!="\n":
                query_appening+=i
            if i=="'":
                flag=True
                continue
            if flag==True:
                if i=="'":
                    flag==False
            if flag==False and i==";":
                query_list.append(query_appening)
                query_appening = ""
        if len(query_list)==0:
            query_list.append(f"{Query_text.get('0.0',END)};")
        query_tabs=CTkTabview(Output_frame)
        query_tabs.pack()

        try:
            for i in range(len(query_list)):
                query_tabs.add(f"Result{i+1}")

                Output_text = Text(query_tabs.tab(f"Result{i+1}"), height=300, width=1000, foreground="white", bg="#333333")
                Output_text.pack()

                Cursor.execute(f"{query_list[i]}")

                try:
                    heading=[element[0] for element in Cursor.description]
                    list_data=[element for element in Cursor.fetchall()]
                    output=tabulate(list_data,headers=heading,tablefmt="grid")
                    Output_text.insert(END,f"{output}\n")
                    try:
                        Connection.commit()
                    except:
                        pass
                except:
                    Output_text.insert(END,"Query OK")
        except Exception as e:
            Output_text.insert(END,f"Error:-{e}")



    Run=CTkButton(query_app,text="Run Query",command=Run_query,height=10,fg_color="transparent",hover_color="red")
    Run.place(x=0,y=0)
    Query_text=Text(query_frame,height=300,width=1000,foreground="white",bg="#333333")
    Query_text.pack()

    Output_frame=CTkScrollableFrame(query_app,height=500,width=1350)
    Output_frame.place(x=0,y=400)
    query_app.mainloop()

def __main__():
    global dictionary_databases,Cursor,Database_frame,main_frame,list_of_table_frame,label_table_database_inuse,desc_frame,Data_frame,desc_label_table,data_label,query_mode
    app.state("zoomed")

    app.resizable(True,True)
    for i in app.winfo_children():
        i.destroy()

    query_mode=CTkButton(app,text="Query_mode",command=Query_mode,height=10,fg_color="transparent",hover_color="red")
    query_mode.place(x=1200,y=0)

    Database_frame=CTkScrollableFrame(app,height=100,width=320)
    Database_frame.place(x=0,y=30)
    CTkLabel(app,text="DATABASES",anchor="w").place(x=0,y=0)

    desc_label_table=CTkLabel(app,text="DESC TABLE")
    desc_label_table.place(x=370 ,y=20)

    desc_frame=CTkScrollableFrame(app,height=250,width=950)
    desc_frame.place(x=370,y=60)

    data_label=CTkLabel(app,text="DATA")
    data_label.place(x=370,y=335)
    Data_frame=CTkScrollableFrame(app,height=300,width=950)
    Data_frame.place(x=370,y=370)

    label_table_database_inuse=CTkLabel(app,text="TABLES",anchor="w")
    label_table_database_inuse.place(x=0,y=240)
    list_of_table_frame=CTkScrollableFrame(app,width=320,height=428)
    list_of_table_frame.place(x=0,y=270)

    Cursor=Connection.cursor()
    Cursor.execute("SHOW DATABASES;")

    control_row_variable=1

    dictionary_databases={i[0]:CTkButton(Database_frame,text=i[0],hover_color="red",fg_color="transparent",anchor="w") for i in Cursor.fetchall()}
    for i in dictionary_databases:
        button_handler=Database_selection(dictionary_databases[i])
        dictionary_databases[i].bind("<Button-1>",button_handler)
        dictionary_databases[i].grid(row=control_row_variable,column=0)
        control_row_variable+=1


if __name__=="__main__":
    connect_to_mysql()
    dictionary_session_buttons = {}
    Button_session_clicked=[]

    try:
        with open(r"D:\GOKUL PERSONAL\python prog\MYSQL EDITOR-SELF\mysql~editor session.dat","rb") as file:
            session_list = []

            try:
                while True:
                    lst = load(file)
                    session_list.append(lst)
            except:
                for i in session_list:
                    for j in list(i.keys()):
                        dictionary_session_buttons[j[0] + str(j[1])] = CTkButton(session_frame,text=f"{j[0] + str(j[1])}",fg_color="transparent",anchor="center",hover_color="red")

                check_colour =False
                for i in dictionary_session_buttons.values():
                    button_click_handler=session_manager(i)
                    i.bind("<Button-1>",button_click_handler)
                    i.pack()
                    if i.cget("fg_color")=="red":
                        check_colour=True
                        break
                if check_colour==True:
                    pass
                else:
                    for child in Login_frame.winfo_children():
                        child.configure(state="disabled")

    except FileNotFoundError:
        with open(r"D:\GOKUL PERSONAL\python prog\MYSQL EDITOR-SELF\mysql~editor session.dat","wb"):
            session_list = []

    app.mainloop()