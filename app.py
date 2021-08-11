import tkinter as tk                    
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename,askdirectory
import os
import sys
sys.path.extend(['scrapy','zingmp3'])

root = tk.Tk()
root.title("Crawler")
root.geometry("500x180")
tabControl = ttk.Notebook(root)
  
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
  
tabControl.add(tab1, text ='Normal')
tabControl.add(tab2, text ='ZingMP3')
tabControl.pack(expand = 1, fill ="both")
  
save = tk.BooleanVar()
info = tk.BooleanVar()
lyric = tk.BooleanVar()
index = tk.BooleanVar()
output = ''
log = ''
depth = 1

# NORMAL URL
###################################################################################
def crawl_normal():
    # print(save.get())
    # print(output)
    command = "python scrapy/main.py"
    
    url=url_txt.get("1.0",tk.END).replace('\n','')
    command += ' ' + url

    ext = ext_txt.get("1.0",tk.END).replace('\n','')
    command += ' -e ' + ext

    depth = depth_txt.get("1.0",tk.END).replace('\n','')
    if depth != '': command += ' -d ' + depth

    if save.get(): command += ' -s'
    if output != '': command += ' -o ' + output
    if log != '': command += ' -l ' + log

    print(command)
    os.system(command)



def set_output():
    global output
    output = askdirectory()
    output_label.configure(text=output)

def set_log():
    global log
    log = askdirectory()
    log_label.configure(text=log)
    log = os.path.join(log,"log.csv")


url_label = ttk.Label(tab1, text = "url")
url_txt = tk.Text(tab1,height=1.5,width=51)
ext_label = ttk.Label(tab1, text = "ext")
ext_txt = tk.Text(tab1,height=1.5,width=30)
depth_label = ttk.Label(tab1, text= "depth")
depth_txt = tk.Text(tab1,height=1.5,width=10)


crawl_btn = tk.Button(tab1, text ="Start", command = crawl_normal)
save_btn = tk.Checkbutton(tab1, text="Save", variable=save)
output_btn = tk.Button(tab1, text="Output Path", command=set_output)
output_label = ttk.Label(tab1)
log_btn = tk.Button(tab1, text="Log Path   ", command=set_log)
log_label = ttk.Label(tab1)


url_label.grid(column = 0, row = 0, pady=(10,0))
url_txt.grid(row=0, column=1, padx = 10, pady=(10,0), sticky='w')
ext_label.grid(column = 0, row = 1)
ext_txt.grid(row=1, column=1, padx = 10, sticky='w')
depth_label.grid(row=1,column=1, sticky='w', padx=(250,0))
depth_txt.grid(row=1, column = 1, sticky='e', padx=(0,10))

output_btn.grid(row=2,column=0,padx=(5,0), sticky='w')
output_label.grid(row=2,column=1,padx=5,pady=5, sticky='w')

log_btn.grid(row=3,column=0,padx=(5,0), sticky='w')
log_label.grid(row=3,column=1,padx=5,pady=5, sticky='w')

save_btn.grid(row=4,column=0,pady=5, padx = 5,sticky="w")

crawl_btn.grid(row=4,column=1)
###################################################################################



#ZingMP3
###################################################################################
def set_zingmp3_output():
    global output
    output = askdirectory()
    output_zingmp3_label.configure(text=output)

def set_zingmp3_log():
    global log
    log = askdirectory()
    log_zingmp3_label.configure(text=log)
    log = os.path.join(log,"log.csv")


def crawl_zingmp3():
    # print(save.get())
    # print(output)
    command = "python zingmp3/main.py"
    
    url=url_zingmp3_txt.get("1.0",tk.END).replace('\n','')
    command += ' ' + url

    if save.get(): command += ' -s'
    if info.get(): command += ' -i'
    if lyric.get(): command += ' -l'
    if index.get(): command += ' --add-index'
    if output != '': command += ' -o ' + output
    if log != '': command += ' --log ' + log

    print(command)
    os.system(command)



url_zingmp3_label = ttk.Label(tab2, text = "url")
url_zingmp3_txt = tk.Text(tab2,height=3,width=50)


crawl_zingmp3_btn = tk.Button(tab2, text ="Start", command = crawl_zingmp3)
save_zingmp3_btn = tk.Checkbutton(tab2, text="Save", variable=save)
info_zingmp3_btn = tk.Checkbutton(tab2, text="Info", variable=info)
lyric_zingmp3_btn = tk.Checkbutton(tab2, text="Lyric", variable=lyric)
index_zingmp3_btn = tk.Checkbutton(tab2, text="Index", variable=index)
output_zingmp3_btn = tk.Button(tab2, text="Output Path", command=set_zingmp3_output)
output_zingmp3_label = ttk.Label(tab2)
log_zingmp3_btn = tk.Button(tab2, text="Log Path   ", command=set_zingmp3_log)
log_zingmp3_label = ttk.Label(tab2)

url_zingmp3_label.grid(column = 0, row = 0, pady=(10,0))
url_zingmp3_txt.grid(row=0, column=1, padx = 10, pady=(10,0), sticky='w')

output_zingmp3_btn.grid(row=2,column=0,padx=(5,0), sticky='w')
output_zingmp3_label.grid(row=2,column=1,padx=5,pady=5, sticky='w')

log_zingmp3_btn.grid(row=3,column=0,padx=(5,0), sticky='w')
log_zingmp3_label.grid(row=3,column=1,padx=5,pady=20, sticky='w')

save_zingmp3_btn.grid(row=4,column=1,pady=5, padx = (5,0),sticky="w")
info_zingmp3_btn.grid(row=4,column=1,pady=5, padx = (50,0),sticky="w")
lyric_zingmp3_btn.grid(row=4,column=1,pady=5, padx = (100,0),sticky="w")
index_zingmp3_btn.grid(row=4,column=1,pady=5, padx = (150,0),sticky="w")

crawl_zingmp3_btn.grid(row=4,column=1, padx=(0,10), sticky='e')
###################################################################################

root.mainloop()  