from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
 
root = Tk()
root.title("CCF compiler")
root.geometry("300x300")
global netDone
global partDone
global netAdded,partAdded
netAdded , partAdded = False, False
def open_net():
    global netDone
    global netAdded
    netFile = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("txt files", "*.txt"),
                                          ("all files", "*.*")))
    netdata = open(netFile,'r')
    netlines = netdata.read()

    datas = netlines.split('\n')
    netDone = []
    for data in datas:
        data.split('\r')
        data = data.split()
        if len(data) != 0 and data[0][0] == '/':
            data[0] = data[0] + '   :   '
            netDone.append(data[0])
            temp=[]
            if '/' not in data[1:]:
                netDone[-1] += ','.join(data[1:])
            else:
                print(' '.join(data[1:4]))
                temp.append(' '.join(data[1:4]))
                temp += data[4:]
                netDone[-1] += ','.join(temp)
        elif len(data) != 0:
            netDone[-1] += ','.join(data)
    netDone = '\n'.join(netDone)
    if len(netFile) !=0:
        netAdded = True
        open_button.config(text = "Net Added!", bg ="green")
    netdata.close()
    print(netDone)
    net_label.config(text = netFile,bg="green")
def open_part():
    global partDone
    global partAdded
    memo = {}
    partFile = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("txt files", "*.txt"),
                                          ("all files", "*.*")))
    partdata = open(partFile,'r')
    partlines = partdata.read()
    datas = partlines.split('\n')
    partDone = []
    for data in datas:
        data.split('\r')
        data = data.split()
        if len(data)!=0 and data[1] not in memo:
            if len(data) == 7:
                memo[data[3]]=[' '.join(data[:3])]
            else:
                memo[data[1]] = [data[0]]
        elif len(data)!=0 :
            if len(data) == 7:
                memo[data[3]].append(' '.join(data[:3]))
            else:
                memo[data[1]].append(data[0])
    for key in memo.keys():
        name = key
        name = name + '   :   '
        li = list(memo[key])
        
        name += ','.join(li)
        name += ';'
        partDone.append(name)
    partDone = '\n'.join(partDone)
    print(partDone)
    if len(partFile) != 0:
        partAdded = True
        open_button2.config(text = "Part Added!", bg ="green")
    partdata.close()
    part_label.config(text = partFile,bg="green")
def make_ccf():
    global netAdded
    global partAdded
    CCF = []
    result = ['$CCF {\nDEFINITION {\n']
    result += partDone
    result += ['\n}\n']
    result += ['NET {\n']
    result += netDone
    result += ['}\n}']
    result = ''.join(result)


    if not netAdded or not partAdded:
        messagebox.showerror(title=None, message="File Not Added",)

    elif netAdded and partAdded:
        filename = filedialog.asksaveasfilename(initialdir = "/", title= "select folder",
        filetypes =(("ccf files","*.ccf"),("all files", "*.*")))
        f = open(filename,'w')
        f.write(result)
        f.close()
        make_ccf.config(text = "Finished!",bg = "green")

    
net_label = Label(root,text = "Net File Not Yet Added",bg="white",padx = 5)
net_label.pack(pady=15)
part_label = Label(root,text = "Part File Not Yet Added",bg="white",padx = 5)
part_label.pack(pady=15)
open_button =  Button(root, text="Add Net File", command = open_net)
open_button2 =  Button(root, text="Add Part File", command = open_part)
open_button.pack(pady = 15)
open_button2.pack(pady = 15)
make_ccf = Button(root, text ="Make CCF File",command = make_ccf)
make_ccf.pack(pady = 15)
root.mainloop()