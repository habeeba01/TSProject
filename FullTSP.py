import tkinter as tk
from tkinter import *
from tkinter import filedialog
import pandas as pd 
import sys
import copy



my_w = tk.Tk()
my_w.geometry("700x700")  # Size of the window 
my_w.title('dynamic project')


l1 = tk.Label(my_w,text='Importer votre fichier excel',width=30)  
l1.grid(row=0,column=1)
b1 = tk.Button(my_w, text='Upload Excel File', 
   width=20,command = lambda:upload_file())
b1.grid(row=1,column=1) 
t1 = tk.Text(my_w, height=30, width=70,bg='pink') # added one text box
t1.grid(row=2,column=1,pady=10) 
#global v
v = tk.IntVar()
tk.Label(my_w, 
        text="""Choose a 
programming method:""",
        justify = tk.LEFT,
        padx = 20).grid()

def upload_file():
    file = filedialog.askopenfilename(
    filetypes=[("Excel file", ".xlsx")])
    mat=pd.read_excel(file) 
    t1.insert(tk.END, mat)
    mat=mat.drop(mat.columns[[0]],axis=1)
    #mat = mat.to_numpy()
    mat=mat.values.tolist()
    return mat

matrice=upload_file()
data={}
for i in range(len(matrice)):
    data[i+1]=str(i+1)
print(matrice)
print(data)
#get ville depart heuristqiue
def getVille():
    global screen1
    screen1=Toplevel(my_w)
    screen1.title("MÉTHODE HEURISTQIUE")
    screen1.geometry("400x400")
    global ville_d
    global ville_départ_entry
    ville_d=StringVar()
    Label(screen1,text="veuillez entrer la ville de départ ").grid()
    ville_départ_entry= Entry(screen1,textvariable=ville_d)
    ville_départ_entry.grid()
    Button(screen1,text="entrer",width=10,height=1,command=lambda:glouton(matrice,data)).grid()
#get ville depart dynamique
def getVillee():
    global screen1
    screen1=Toplevel(my_w)
    screen1.title("PROGRAMMATION DYNAMIQUE")
    screen1.geometry("400x400")
    global ville_d
    global ville_départ_entry
    ville_d=StringVar()
    Label(screen1,text="veuillez entrer la ville de départ ").grid()
    ville_départ_entry= Entry(screen1,textvariable=ville_d)
    ville_départ_entry.grid()
    Button(screen1,text="entrer",width=10,height=1,command=lambda:main(matrice)).grid()
#HEURISTIQUE
'''Fonction qui calcule le transposée'''
def transpose(matrixx):
    if matrixx == None or len(matrixx) == 0:
        return []
        
    result = [[None for i in range(len(matrixx))] for j in range(len(matrixx[0]))]
    
    for i in range(len(matrixx[0])):
        for j in range(len(matrixx)):
            result[i][j] = matrixx[j][i]
            
    return result
#Le plus proche voisin
def glouton(matriceDistance,names):
    sol=[]
    ville_départ=ville_d.get()
    ville_départ_entry.delete(0,END)
    #ville_départ = input("ville départ : ")
   
    vdd = ville_départ
    vd = 1
    l = []
    for cle,value in names.items():
        if ville_départ == value:
            vd = cle
            for i in range(len(matriceDistance)):
                tmp2 = matriceDistance[i][0]
                matriceDistance[i][0] = matriceDistance[i][vd-1]
                matriceDistance[i][vd-1] = tmp2
            for j in range(len(matriceDistance[i])):
                tmp = matriceDistance[0][j]
                matriceDistance[0][j] = matriceDistance[vd-1][j]
                matriceDistance[vd-1][j] = tmp       
    names[vd] = names[1]
    tmm = names[1]
    names[1] = ville_départ
    ville_départ = tmm
    #print(names[1])
    #print(matriceDistance)
    #print(names)
    liste = [name for name in names]
    solutionConstruite = [1]
    liste.pop(0)
    while len(liste)>0:
        u = solutionConstruite[-1]
        v = liste[-1]
        distance = float("inf")
        for w in liste:
            if matriceDistance[u-1][w-1] < distance:
                distance = matriceDistance[u-1][w-1]
                v = w
        solutionConstruite.append(v)
        liste.remove(v)
    #solutionConstruite.append(1)
    #print('\n\nSolution to TSP heuristique : {',names[1],',', end='')
    sol.append(names[1])
    if transpose(matriceDistance) != matriceDistance:
        solutionConstruite.reverse()
        for i in solutionConstruite :
            for cle,value in data.items():
                if i == cle :
                    vi = value
                    #print(vi, end=', ')
                    sol.append(vi)
        #print('}')
    else :
        for i in solutionConstruite :
            for cle,value in data.items():
                if i == cle :
                    vi = value
                    #print(vi, end=', ')
                    l.append(vi)
        l.reverse()
        #print(l,'}')
        sol.append(l)
    #print(sol)
    Label(screen1,text=sol,fg="green").grid()
    return 'Solution to TSP heuristique :',sol

btnn = tk.Button(my_w, text="heuristique", command =lambda:getVille())
btnn.grid()

#DYNAMIQUE SOLUTION
n = len(data)
all_sets = []
g = {}
p = []
s=[]
def main(mat):
    ville_départ=ville_d.get()
    ville_départ_entry.delete(0,END)
    #ville_départ = input("ville départ : ")
    vdd = ville_départ
    for cle,value in data.items():
        if ville_départ == value:
            vd = cle
            for i in range(len(mat)):
                tmp2 = mat[i][0]
                mat[i][0] = mat[i][vd-1]
                mat[i][vd-1] = tmp2
            for j in range(len(mat[i])):
                tmp = mat[0][j]
                mat[0][j] = mat[vd-1][j]
                mat[vd-1][j] = tmp       
    data[vd] = data[1]
    tmm = data[1]
    data[1] = ville_départ
    ville_départ = tmm
   # print(data[1])
    for x in range(1, n):
        g[x + 1, ()] = mat[x][0]
    print(data)
    print(mat)
    data.pop(1)
    
    get_minimumm(vd, tuple(data), mat)
    #print('\n\nSolution du TSP: {',vdd,',', end='')
    s.append(vdd)
    solution = p.pop()
    for cle,value in data.items():
        if cle == solution[1][0]:
            vi = value
            #print(vi, end=', ')
            s.append(vi)
            break
    for x in range(n - 2):
        for new_solution in p:
            if tuple(solution[1]) == new_solution[0]:
                solution = new_solution
                for cle,value in data.items():
                    if cle == solution[1][0]:
                        vi = value
                #print(vi, end=', ')
                s.append(vi)
                break
    #print(vdd,'}')
    s.append(vdd)
    #print(s)
    Label(screen1,text=s,fg="green").grid()
    return 'Solution du TSP:',s
   
def get_minimumm(k, a, mat):
    if (k, a) in g:
        return g[k, a]

    values = []
    all_min = []
    for j in a:
        set_a = copy.deepcopy(list(a))
        set_a.remove(j)
        all_min.append([j, tuple(set_a)])
        result = get_minimumm(j, tuple(set_a), mat)
        values.append(mat[k-1][j-1] + result)


    g[k, a] = min(values)
    p.append(((k, a), all_min[values.index(g[k, a])]))
    return g[k, a]
btn = tk.Button(my_w, text="dynamique", command =lambda:getVillee())
btn.grid()

my_w.mainloop()  # Keep the window open