from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize,sent_tokenize
from nltk.collections import Counter

import os


win=Tk()
win.title("Text Summerization")



string_summ = ''
show_text_val = 0
scroll = None
text_entry = None
frame2 = None
path_string = StringVar()
no_words=IntVar()
no_words.set('1')



def summerize_text(text,des_path,n):
    try:
        # deleting all punctuation marks
        text=text.replace('. ','.')
        text=text.replace('.','. ')
        for i in range(0,1114112):
            if (i>48 and i<58) or (i>64 and i<91) or (i>96 and i<123) or i==32 or i==46:
                pass
            else:
                text=text.replace(chr(i),'')

        # spliting lines and adding numbers
        lines=sent_tokenize(text)
                
        # spliting words
        text=text.replace('.','')
        text_words=text.split(' ')
        text_words=[i for i in text_words if len(i)>1]

        # removing stopwords
        stop_words=[]
        important_words=[]
        for i in stopwords.words('english'):
            stop_words.append(i.replace("'",''))
        for i in text_words:
            if i.lower() not in stop_words:
                important_words.append(i)
        
        if n>len(important_words):
            messagebox.showwarning('Warning','You entered number is greater then words in text')
        else:
            # frequncy distirbutor
            word=Counter(important_words)
            word_frequency=word.most_common(n)

            # getting frequncy repeated lines
            important_lines=[]
            for i in lines:
                for j in word_frequency:
                    for z in i.split(' '):
                        if j[0]==z and i not in important_lines:
                            important_lines.append(i)

            # saving to file
            with open(des_path+'/output.txt','w') as file:
                for i in important_lines:
                    if important_lines.index(i)==0:
                        file.write(i)
                    else:
                        file.write(' '+i)
            messagebox.showinfo("File Saved","Summeriaze file is saved at:{}".format(os.path.dirname(path_string.get())+'/output.txt'))
            return True
    except Exception as e:
        print(e)


def open_file():
    global string_summ
    try:
        path = filedialog.askopenfile(title="Open File",filetypes=(("text files",'.txt'),('all files','*.*')),defaultextension=("text files",'.txt'),initialdir="C:/")
        path = path.name
        file2 = open(path)
        string_summ = file2.read()
        no_com.config(state='active')
        summ_btn.config(state='active')
        path_string.set(path)
        path_En.config(state='disabled')
    except Exception as e:
        print(e)



def show_text():
    global show_text_val,scroll,text_entry,frame2
    if show_text_val == 0:
        frame2=Frame(bg="powder blue")
        frame2.pack(pady=(10,0))
        scroll = Scrollbar(frame2)
        scroll.pack(side="right",fill=Y)
        text_entry = Text(frame2,width="42",height="10",yscrollcommand=scroll.set,wrap='word')
        text_entry.pack()
        file=open(os.path.dirname(path_string.get())+'/output.txt','r')
        text_entry.insert(1.0,file.read())
        text_entry.config(state="disabled")
        scroll.config(command=text_entry.yview)
        show_text_val = 1
    elif show_text_val == 1:
        frame2.destroy()
        scroll.destroy()
        text_entry.destroy()
        show_text_val = 0



def summ_file():
    file=open(path_string.get())
    if summerize_text(file.read(),os.path.dirname(path_string.get()),no_words.get()):
        show_btn = ttk.Button(frame,text="Show Text",command=show_text)
        show_btn.grid(row=5,column=0,columnspan=2,pady=(10,0))
        hide_btn = ttk.Button(frame,text="Hide Text",command=show_text)
        hide_btn.grid(row=6,column=0,columnspan=2,pady=(10,0))



def win_exit():
    boo=messagebox.askyesno("Exit","Are you sure to exit")
    if boo:
        win.destroy()



win.geometry("600x500")
win.resizable(0,0)
win.config(bg="powder blue")

frame = Frame(bg="powder blue")
frame.pack(pady=(10,0))

lb=Label(frame,text="Text Summerization",font=('times',24,'bold'),bg='powder blue',fg='red')
lb.grid(row=0,columnspan=2)

path_En = ttk.Entry(frame,width="42",textvariable=path_string)
path_En.grid(row=1,column=0)

path_btn = ttk.Button(frame,text="Open File",command = open_file)
path_btn.grid(row=1,column=1,padx=(10,0))

no_label=Label(frame,text="No Of Words:",bg='powder blue')
no_label.grid(row=2,columnspan=2,pady=(10,0))
no_com = ttk.Entry(frame,textvariable=no_words,state='disabled')
no_com.grid(row=3,columnspan=2)

summ_btn = ttk.Button(frame,text="Summeraize",command = summ_file,state='disabled')
summ_btn.grid(row=4,column=0,columnspan=2,pady=(10,0))

win.protocol("WM_DELETE_WINDOW",win_exit)
win.mainloop()
