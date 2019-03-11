import sqlite3
import random
from tkinter import *	
from bs4 import BeautifulSoup
import requests

def finish():
	window.destroy()
	results=Tk(className=" Results")
	results.resizable(False, False)
	results.geometry()
	last=Text(results,height=20,width=45,background="DarkOliveGreen3",fg="white",font="Helvetica 12 bold")
	last.grid(row=0,column=0)
	last.delete("1.0 ", END)
	for x in corr:
		last.insert(END,x[0]+" <==> "+x[1]+"\n")
	last.config(state="disabled")
	last2=Text(results,height=20,width=45,background="LightSalmon3",fg="white",font="Helvetica 12 bold")
	last2.grid(row=0,column=20)
	last2.delete("1.0 ",END)
	for x in wro:
		last2.insert(END, x[0]+" <==> "+x[1]+"\n")
	last2.config(state="disabled")	
	results.mainloop()

def mainfun(maxnum,words):
	global buton1, buton2, buton3, correctnum, bt1,bt2,bt3,corr,wro
	firstbutton1.destroy()
	firstbutton2.destroy()
	firstbutton3.destroy()
	first=Text(window,height=2,width=23,background="RosyBrown3",fg="white",font="Helvetica 14 bold")#sorulan kelime
	first.grid(row=0,column=7)
	first.delete("1.0 ", END)
	correctnum=random.randint(0,maxnum-1)
	num=[]
	num.append(random.randint(0,maxnum-1))
	num.append(correctnum)
	num.append(random.randint(0,maxnum-1))
	numfor=random.randint(0,2)
	first.insert(END,words[correctnum][0])
	first.tag_configure("center", justify='center')
	first.tag_add("center", 1.0, "end")
	bt1=Button(window,command=lambda: fun(words),text=words[num[numfor]][1],height=2,width=30)
	bt1.grid(row=8,column=5)
	buton1=num.pop(numfor)
	numfor=random.randint(0,1)
	bt2=Button(window,command=lambda: fun2(words),text=words[num[numfor]][1],height=2,width=30)
	bt2.grid(row=8,column=7)
	buton2=num.pop(numfor)
	bt3=Button(window,command=lambda: fun3(words),text=words[num[0]][1],height=2,width=30)
	bt3.grid(row=8,column=9)
	buton3=num[0]

def fun(words):#1.butonun fonksiyonu
	if correctnum==buton1:
		bt1.config(background="DarkOliveGreen3")
		corr.append(words[correctnum])
		words.pop(correctnum)
	else:
		wro.append(words[correctnum])
		bt1.config(background="LightSalmon3")
		if correctnum==buton2:
			bt2.config(background="DarkOliveGreen3")
		else:
			bt3.config(background="DarkOliveGreen3")
	bt1.config(state="disabled")
	bt2.config(state="disabled")
	bt3.config(state="disabled")		
	cbt=Button(window,text="Continue",command=lambda: mainfun(len(words),words),font="Helvetica 10")
	cbt.grid(row=10,column=7)			
	fns=Button(window,text="Finish",command=finish,font="Helvetica 10")			
	fns.grid(row=12,column=7)	

def fun2(words):#2.butonun fonksiyonu
	if correctnum==buton2:
		bt2.config(background="DarkOliveGreen3")
		corr.append(words[correctnum])
		words.pop(correctnum)
	else:
		wro.append(words[correctnum])
		bt2.config(background="LightSalmon3")	
		if correctnum==buton1:
			bt1.config(background="DarkOliveGreen3")
		else:
			bt3.config(background="DarkOliveGreen3")
	bt1.config(state="disabled")
	bt2.config(state="disabled")
	bt3.config(state="disabled")			
	cbt=Button(window,text="Continue",command=lambda: mainfun(len(words),words),font="Helvetica 10")
	cbt.grid(row=10,column=7)
	fns=Button(window,text="Finish",command=finish,font="Helvetica 10")			
	fns.grid(row=12,column=7)	

def fun3(words):#3.butonun fonksiyonu
	if correctnum==buton3:
		bt3.config(background="DarkOliveGreen3")
		corr.append(words[correctnum])
		words.pop(correctnum)
	else:
		wro.append(words[correctnum])
		bt3.config(background="LightSalmon3")
		if correctnum==buton2:
			bt2.config(background="DarkOliveGreen3")
		else:
			bt1.config(background="DarkOliveGreen3")
	bt1.config(state="disabled")
	bt2.config(state="disabled")
	bt3.config(state="disabled")	
	cbt=Button(window,text="Continue",command=lambda: mainfun(len(words),words),font="Helvetica 10")
	cbt.grid(row=10,column=7)	
	fns=Button(window,text="Finish",command=finish,font="Helvetica 10")			
	fns.grid(row=12,column=7)
#main başlangıcı
con=sqlite3.connect("datum.db")
cur=con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS datum (name TEXT)")	
cur.execute("CREATE TABLE IF NOT EXISTS data (name TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS data2 (name TEXT)")
cur.execute("SELECT * FROM datum")
empty=cur.fetchall()
#dosyanın içi alındı
if len(empty)==0 :#dosya boş ise
	x=requests.get('https://www.tipfak.com/tibbi-ingilizce-kelime-bankasi/')
	soup=BeautifulSoup(x.text,"html.parser")
	s=soup.find_all("p")
	words=[]
	for a in s:
		if ":" in a.text:
			ilk=a.text
			words.append(ilk.split(":"))
	#1.scrape		
	x1=requests.get('http://www.almancaegitim.net/almanca-tibbi-terimler.html')
	soup1=BeautifulSoup(x1.text,"html.parser")
	s1=soup1.find_all("p")
	s1.pop(-1)
	s1.pop(-1)
	almwords=[]
	for a in s1:
		mean=a.text
		real=mean.split('.')
		for re in real:
			if len(re)!=0:
				almwords.append(re.split('/'))	
	for a in almwords:
		if "Arzt" in a[0]:
			a[1]="Doktor"
		if "\n" in a[0]:
			a[0]=a[0][1:]			
	#2.scrape
	x2=requests.get('http://www.101languages.net/german/german-word-list/')
	soup2=BeautifulSoup(x2.text,"html.parser")
	s2=soup2.find_all("td")
	listfor=[]
	listformean=[]
	i=0
	for a in s2:
		if i%2==0:
			listformean.append(a.text)
		else: 
			listfor.append(a.text)
		i+=1
	resultgerm=list(zip(listfor,listformean))
	#3.scrape	
	for word in words:
		wor=word[0]+"_"+word[1]
		cur.execute("INSERT INTO datum VALUES(?)", (wor,))	
	for almw in almwords:
			if len(almw) > 1:
				alm=almw[0]+"_"+almw[1]
				cur.execute("INSERT INTO data VALUES(?)",(alm,))
	for almw in resultgerm:
		alm=almw[0]+"_"+almw[1]
		cur.execute("INSERT INTO data2 VALUES(?)",(alm,))
	con.commit()
	con.close()
	#db yazdırma	
else:#dosya dolu ise
	words=[]
	almwords=[]
	resultgerm=[]
	cur.execute("SELECT * FROM datum")
	rows=cur.fetchall()
	for word in rows:	
		word=str(word[0])
		word=word.split("_")
		words.append(word)	
	cur.execute("SELECT * FROM data")
	rows=cur.fetchall()
	for word in rows:
		word=str(word[0])
		word=word.split("_")
		almwords.append(word)
	cur.execute("SELECT * FROM data2")
	rows=cur.fetchall()
	for word in rows:
		word=str(word[0])
		word=word.split("_")	
		resultgerm.append(word)
	con.commit()
	con.close()	
	#db veri alma
corr=[]
wro=[]#doğru yanlışları tutan listeler
window=Tk(className=" Word App for Esmos")
window.config(background="pink")
window.geometry('662x240')
window.resizable(False, False)

firstbutton1=Button(window,text="English Words",command=lambda: mainfun(len(words),words),font="Helvetica 10 bold")
firstbutton1.pack(side="top", fill='both', padx=20, pady=18)
firstbutton1.config(height=2,width=20,background="red2",foreground="light cyan")
firstbutton2=Button(window,text="German Medicine Words",command=lambda: mainfun(len(almwords),almwords),font="Helvetica 10 bold")
firstbutton2.pack(side="top", fill='both', padx=20, pady=18)
firstbutton2.config(height=2,width=20,background="orange2",foreground="light cyan")
firstbutton3=Button(window,text="German General Words",command=lambda: mainfun(len(resultgerm),resultgerm),font="Helvetica 10 bold")
firstbutton3.pack(side="top", fill='both', padx=20, pady=18)
firstbutton3.config(height=2,width=20,background="orange3",foreground="light cyan")

window.mainloop()
	

