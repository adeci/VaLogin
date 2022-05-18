import subprocess
from tkinter import *
from tkinter import ttk
from pynput.keyboard import Key, Controller
from functools import partial
import time
import psutil
import threading
from ctypes import windll
import pygetwindow as gw

keyboard = Controller()

def getinfo():
    global count
    global names
    global user
    global passw
    count = 0
    user = []
    passw = []
    names = []
    with open('accounts.csv') as f:
        for line in f:
            acclst = line.split()
            names.append(acclst[0])
            user.append(acclst[1])
            passw.append(acclst[2])
            acclst.clear()
            count += 1

def account(i):
    root.destroy()
    username = user[i]
    password = passw[i]
    t1=threading.Thread(target=startProg)
    t1.daemon = True
    t1.start()
    while True:
        if checkIfProcessRunning('RiotClientUx'):
            #wait a few seconds, if process tries to bring window to front
            #that is not initialized yet program will crash
            time.sleep(3)
            #bring window to front
            win = gw.getWindowsWithTitle('Riot Client Main')[0]
            win.activate()

            #type creds
            keyboard.type(username)
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            keyboard.type(password)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            break

def startProg():
    subprocess.call(['C:\Riot Games\Riot Client\RiotClientServices.exe' ,'--launch-product=valorant' ,'--launch-patchline=live'])
def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def final():
    root.destroy()

def butstate():
    sett.destroy()
    setbut["state"] = "normal"

def update(data):
    setbox.delete(0, 'end')
    for item in data:
        setbox.insert('end', item)

def chosen(event):
    global sel
    try:
        sel = setbox.get(setbox.curselection())
    except:
        sel = ''
    if sel != '':
        namepick.config(text = sel)
        delbut["state"] = "normal"

def killacc():
    for i in range(len(names)):
        if sel == names[i]:
            with open("accounts.csv", "r") as f:
                lines = f.readlines()
            with open("accounts.csv", "w") as f:
                lcount = 0
                for line in lines:
                    if lcount != i:
                        if line == lines[-1]:
                            f.write(line.rstrip())
                        else:
                            f.write(line)
                    lcount += 1
            rewritewidgets()
            delbut["state"] = "disabled"
            namepick.config(text = "Choose Account")
            getinfo()
            update(names)
            break

def addacc():
    addbutt["state"] = "disabled"
    with open("accounts.csv", "r") as f:
        lines = f.readlines()
        print(lines)
    with open("accounts.csv", "a") as f:
            f.write(newname + ' ' + newuser + ' ' + newpass)
            f.write("\n")
    namee.delete(0, END)
    usere.delete(0, END)
    passe.delete(0, END)

    rewritewidgets()
    getinfo()
    update(names)

def settings():
    #disable buttone
    setbut["state"] = "disabled"

    #define new window
    global sett
    sett = Toplevel(root)

    sett.title("Settings")
    sett.geometry("780x280")
    sett.iconphoto(False, PhotoImage(file='icon.png'))
    sett.attributes("-topmost", True)

    sett.update()
    sett.minsize(sett.winfo_width(), sett.winfo_height())
    x_cordinate = int((sett.winfo_screenwidth() / 2) - (sett.winfo_width() / 2))
    y_cordinate = int((sett.winfo_screenheight() / 2) - (sett.winfo_height() / 2))
    sett.geometry("+{}+{}".format(x_cordinate+40, y_cordinate-110))

    sett.protocol("WM_DELETE_WINDOW", butstate)

    #widgets
    boxframe = ttk.Frame(sett)
    boxframe.grid(row=0,column=0)

    global setbox
    setbox = Listbox(boxframe, width = 50,exportselection=False)
    setbox.grid(row=0,column=0, padx=15,pady=(20,5))
    update(names)
    setbox.bind('<<ListboxSelect>>', chosen)

    eframe = ttk.Frame(sett)
    eframe.grid(row=0,column=1,padx=15,pady=(10,5))

    ignlab = ttk.Label(eframe, text = "IGN")
    ignlab.grid(row =0, column = 0)

    global namee
    namee = ttk.Entry(eframe, width = 50)
    namee.grid(row = 1, column = 0)
    namee.bind('<KeyRelease>', namekey)

    ignlab = ttk.Label(eframe, text = "Username")
    ignlab.grid(row = 2, column = 0)

    global usere
    usere = ttk.Entry(eframe, width = 50)
    usere.grid(row = 3, column = 0)
    usere.bind('<KeyRelease>', userkey)

    ignlab = ttk.Label(eframe, text = "Password")
    ignlab.grid(row = 4, column = 0)

    global passe
    passe = ttk.Entry(eframe, width = 50)
    passe.grid(row = 5, column = 0)
    passe.bind('<KeyRelease>', passkey)

    global namepick
    namepick = ttk.Label(sett, text = "Choose Account")
    namepick.grid(row=1,column=0)

    global delbut
    delbut = ttk.Button(sett, width = 20, text="Delete Account", command=killacc)
    delbut["state"] = "disabled"
    delbut.grid(row=2,column=0)

    global additem
    additem = ttk.Label(sett, text = "Add Name")
    additem.grid(row=1,column=1)

    global addbutt
    addbutt = ttk.Button(sett, width = 20, text="Add Account", command=addacc)
    addbutt["state"] = "disabled"
    addbutt.grid(row=2,column=1)

def namekey(event):
    global newname
    newname = event.widget.get()
    if newname == "":
        additem.config(text = "Account Name")
    additem.config(text = newname)
    try:
        if newname != '' and newuser != '' and newpass != '':
            addbutt["state"] = "normal"
    except:
        pass

def userkey(event):
    global newuser
    newuser = event.widget.get()
    try:
        if newname != '' and newuser != '' and newpass != '':
            addbutt["state"] = "normal"
    except:
        pass

def passkey(event):
    global newpass
    newpass = event.widget.get()
    try:
        if newname != '' and newuser != '' and newpass != '':
            addbutt["state"] = "normal"
    except:
        pass

def drawwidgets():
    label.pack(padx=80, pady=(5,10))
    getinfo()
    #accbuttons
    butframe.pack()
    if count > 0:
        for i in range(0, count):
            b1 = ttk.Button(butframe, width = 20, text=names[i], command=partial(account, i))
            b1.pack(padx=15, pady=(0,5))

    setbut.pack(padx=15, pady=(25,0))
    quitbut.pack(padx=15, pady=(5,15))

def rewritewidgets():
    global butframe

    label.pack_forget()
    setbut.pack_forget()
    quitbut.pack_forget()
    butframe.destroy()
    label.pack(padx=80, pady=(5,10))
    butframe = ttk.Frame(root)
    butframe.pack()
    getinfo()
    if count > 0:
        for i in range(0, count):
            b1 = ttk.Button(butframe, width = 20, text=names[i], command=partial(account, i))
            b1.pack(padx=15, pady=(0,5))
    setbut.pack(padx=15, pady=(25,0))
    quitbut.pack(padx=15, pady=(5,15))

######DEFINE TKINTER WINDOW AND SET WIDGETS#####
root = Tk()
root.overrideredirect(1)
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "dark")
root.attributes('-alpha',0.95)
root.iconphoto(False, PhotoImage(file='icon.png'))
root.title("VaLogin")
root.attributes("-topmost", True)
root.minsize(root.winfo_width(), root.winfo_height())
x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
root.geometry("+{}+{}".format(x_cordinate, y_cordinate-110))
#main widgets
global setbut
global quitbut
butframe = ttk.Frame(root)
label = ttk.Label(root, font = 100,text="VaLogin")
setbut = ttk.Button(root, width = 20, text="Settings", command=settings)
quitbut = ttk.Button(root, width = 20, text="Quit", command=final)
################################################

drawwidgets()

#####WINDOWS TASKBAR DISPLAY RECODE - DO NOT TOUCH#####
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
hwnd = windll.user32.GetParent(root.winfo_id())
stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
stylew = stylew & ~WS_EX_TOOLWINDOW
stylew = stylew | WS_EX_APPWINDOW
res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
root.wm_withdraw()
root.after(10, lambda: root.wm_deiconify())
##############################################################

root.mainloop()