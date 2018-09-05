from gi.repository import Gtk
import string 
import logica
import tkinter
from tkinter import messagebox


############Aqui estan las funciones de cada boton##########
def enable(letra,Dd,Rd,check,Ld,texto):
	letra.set_editable(check.get_active())
	Dd.set_editable(check.get_active())
	Rd.set_editable(check.get_active())
	if check.get_active() == False:
		letra.set_text("")
		Dd.set_text("")
		Ld.set_text("")
		Rd.set_text("")
	else: 
		letra.set_text(texto.upper())
		Ld.set_text(texto.lower())

def enablebutton1(button):
	enable(letra1,Ddescription1,Rdescription1,check_1,Lrecesive1,"A")

def enablebutton2(button):
	enable(letra2,Ddescription2,Rdescription2,check_2,Lrecesive2,"B")

def enablebutton3(button):
	enable(letra3,Ddescription3,Rdescription3,check_3,Lrecesive3,"C")

def enablebutton4(button):
	enable(letra4,Ddescription4,Rdescription4,check_4,Lrecesive4,"D")

def enablebutton5(button):
	enable(letra5,Ddescription5,Rdescription5,check_5,Lrecesive5,"E")

def enablebutton6(button):
	enable(letra6,Ddescription6,Rdescription6,check_6,Lrecesive6,"F")
	


#######Aqui los checks de cada uno ################
def correcto(letra,check,Lrecesive,Ddescription,Rdescription):
	wletter = letra.get_text()
	if wletter in string.ascii_letters and check.get_active():
		Lrecesive.set_text(wletter.lower())
		letra.set_text(wletter.upper())
	else :
		Lrecesive.set_text("")
		letra.set_text("")
		Ddescription.set_editable(False)
		Rdescription.set_editable(False)

def correcto_1(button):
	correcto(letra1,check_1,Lrecesive1,Ddescription1,Rdescription1)

def correcto_2(button):
	correcto(letra2,check_2,Lrecesive2,Ddescription2,Rdescription2)

def correcto_3(button):
	correcto(letra3,check_3,Lrecesive3,Ddescription3,Rdescription3)

def correcto_4(button):
	correcto(letra4,check_4,Lrecesive4,Ddescription4,Rdescription4)

def correcto_5(button):
	correcto(letra5,check_5,Lrecesive5,Ddescription5,Rdescription5)

def correcto_6(button):
	correcto(letra6,check_6,Lrecesive6,Ddescription6,Rdescription6)

### Esto es para guardar. Trabajar mas en ello
def store_info(button):
	global info_alelos
	info_alelos = []
	if check_1.get_active()==True:
		info_alelos.append([letra1.get_text(),Lrecesive1.get_text(), Ddescription1.get_text(), Rdescription1.get_text()])
	if check_2.get_active()==True:
		info_alelos.append([letra2.get_text(),Lrecesive2.get_text(), Ddescription2.get_text(), Rdescription2.get_text()])
	if check_3.get_active()==True:
		info_alelos.append([letra3.get_text(),Lrecesive3.get_text(), Ddescription3.get_text(), Rdescription3.get_text()])
	if check_4.get_active()==True:
		info_alelos.append([letra4.get_text(),Lrecesive4.get_text(), Ddescription4.get_text(), Rdescription4.get_text()])
	if check_5.get_active()==True:
		info_alelos.append([letra5.get_text(),Lrecesive5.get_text(), Ddescription5.get_text(), Rdescription5.get_text()])
	if check_6.get_active()==True:
		info_alelos.append([letra6.get_text(),Lrecesive6.get_text(), Ddescription6.get_text(), Rdescription6.get_text()])
	print(info_alelos)

def get_data():
	global current_data
	current_data = []
	if check_1.get_active()==True:
		current_data.append([letra1.get_text(),Lrecesive1.get_text(), Ddescription1.get_text(), Rdescription1.get_text()])
	if check_2.get_active()==True:
		current_data.append([letra2.get_text(),Lrecesive2.get_text(), Ddescription2.get_text(), Rdescription2.get_text()])
	if check_3.get_active()==True:
		current_data.append([letra3.get_text(),Lrecesive3.get_text(), Ddescription3.get_text(), Rdescription3.get_text()])
	if check_4.get_active()==True:
		current_data.append([letra4.get_text(),Lrecesive4.get_text(), Ddescription4.get_text(), Rdescription4.get_text()])
	if check_5.get_active()==True:
		current_data.append([letra5.get_text(),Lrecesive5.get_text(), Ddescription5.get_text(), Rdescription5.get_text()])
	if check_6.get_active()==True:
		current_data.append([letra6.get_text(),Lrecesive6.get_text(), Ddescription6.get_text(), Rdescription6.get_text()])

def put_data():
	clear(letra1,Ddescription1,Rdescription1,check_1,Lrecesive1)
	clear(letra2,Ddescription2,Rdescription2,check_2,Lrecesive2)
	clear(letra3,Ddescription3,Rdescription3,check_3,Lrecesive3)
	clear(letra4,Ddescription4,Rdescription4,check_4,Lrecesive4)
	clear(letra5,Ddescription5,Rdescription5,check_5,Lrecesive5)
	clear(letra6,Ddescription6,Rdescription6,check_6,Lrecesive6)	
	global current_data
	if len(current_data) > 0: 
		check_1.set_active(True)
		letra1.set_text(current_data[0][0])
		Lrecesive1.set_text(current_data[0][1])
		Ddescription1.set_text(current_data[0][2])
		Rdescription1.set_text(current_data[0][3])
	if len(current_data) > 1: 
		check_2.set_active(True)
		letra2.set_text(current_data[1][0])
		Lrecesive2.set_text(current_data[1][1])
		Ddescription2.set_text(current_data[1][2])
		Rdescription2.set_text(current_data[1][3])
	if len(current_data) > 2: 
		check_3.set_active(True)
		letra3.set_text(current_data[2][0])
		Lrecesive3.set_text(current_data[2][1])
		Ddescription3.set_text(current_data[2][2])
		Rdescription3.set_text(current_data[2][3])
	if len(current_data) > 3: 
		check_4.set_active(True)
		letra4.set_text(current_data[3][0])
		Lrecesive4.set_text(current_data[3][1])
		Ddescription4.set_text(current_data[3][2])
		Rdescription4.set_text(current_data[3][3])
	if len(current_data) > 4: 
		check_5.set_active(True)
		letra5.set_text(current_data[4][0])
		Lrecesive5.set_text(current_data[4][1])
		Ddescription5.set_text(current_data[4][2])
		Rdescription5.set_text(current_data[4][3])
	if len(current_data) > 5: 
		check_6.set_active(True)
		letra6.set_text(current_data[5][0])
		Lrecesive6.set_text(current_data[5][1])
		Ddescription6.set_text(current_data[5][2])
		Rdescription6.set_text(current_data[5][3])

def clear(letra,Dd,Rd,check,Ld):
	check.set_active(False)
	letra.set_text("")
	letra.set_editable(False)
	Dd.set_text("")
	Dd.set_editable(False)
	Ld.set_text("")
	Rd.set_text("")
	Rd.set_editable(False)

def save(button):
	dialog = Gtk.FileChooserDialog("Please choose a file", parent = None, action = Gtk.FileChooserAction.SAVE, buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
	dialog.add_filter(filter_text)
	global file_save
	file_save = dialog.run()
	if file_save == Gtk.ResponseType.OK:
		get_data()
		save2XML(current_data, dialog.get_filename())
	dialog.destroy()

def load(button):
	dialog = Gtk.FileChooserDialog("Please choose a file", parent = None, action = Gtk.FileChooserAction.OPEN, buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
	dialog.add_filter(filter_text)
	global file_load
	file_load = dialog.run()
	if file_load == Gtk.ResponseType.OK:
		global current_data
		current_data = read4XML(dialog.get_filename())
		put_data()
	dialog.destroy()



############################ El boton de analisis da la ssegunda ventan
def analyze_data(button):
	dom_letter = ""
	rec_letter = ""
	if check_1.get_active() == True and letra1.get_text() != "":
		dom_letter = dom_letter + letra1.get_text()
		rec_letter = rec_letter + Lrecesive1.get_text()

	if check_2.get_active() == True:
		dom_letter = dom_letter + letra2.get_text()
		rec_letter = rec_letter + Lrecesive2.get_text()

	if check_3.get_active() == True:
		dom_letter = dom_letter + letra3.get_text()
		rec_letter = rec_letter + Lrecesive3.get_text()

	if check_4.get_active() == True:
		dom_letter = dom_letter + letra4.get_text()
		rec_letter = rec_letter + Lrecesive4.get_text()

	if check_5.get_active() == True:
		dom_letter = dom_letter + letra5.get_text()
		rec_letter = rec_letter + Lrecesive5.get_text()

	if check_6.get_active() == True:
		dom_letter = dom_letter + letra6.get_text()
		rec_letter = rec_letter + Lrecesive6.get_text()

	if len(dom_letter) > 0 and duplicate(dom_letter) == False:
		global lista_fenotipos
		lista_fenotipos = (logica.allPhenotypes(len(dom_letter), dom_letter, rec_letter))
		populate_box(lista_fenotipos , lista_alelos1)
		populate_box(lista_fenotipos , lista_alelos2)
		print (lista_alelos2, lista_fenotipos)
		
		combo1.set_model(lista_alelos1)
		combo2.set_model(lista_alelos2)	
	elif len(dom_letter) > 0 and duplicate(dom_letter) == True:
		##print("Hay letras duplicadas") ## Reemplazar por error o alerta
		root = tkinter.Tk()
		root.withdraw()		
		messagebox.showerror("Error", "Hay letras duplicadas, ingrese los datos de nuevo")
		root.destroy()
	elif len(dom_letter) == 0 :
		##print ("Debe introducir más de 0 alelos") ## reemplazar por error o alerta
		root = tkinter.Tk()
		root.withdraw()		
		messagebox.showerror("Error", "Debe introducir la información de al menos un gen")
		root.destroy()

	
def populate_box(alelos, lista):  ## Esta funcion anade los alelos a las lista despegable
	lista.clear()	
	for i in range(len(alelos)):
			lista.append([alelos[i]])
		

def duplicate(letras):   ##chequea si hay letras duplicadas
	no_dup_str="".join(set(letras))
	if len(no_dup_str)==len(letras):
		return False 
	else:
		return True
## dd = descripcion dominante, dr, descripcion recesiva
def interpret(letras):
	alelos_num = int(len(letras)/2)
	interpret_text = ""
	if alelos_num >0:
		for i in range(len(letras)):
			if i%2==0:
				if letras[i] == letras[i].upper():
					print (i)
					interpret_text += info_alelos[int(i/2)][2] 
					interpret_text += " "
				elif letras[i] == letras[i].lower():
					interpret_text += info_alelos[int(i/2)][3]		
					interpret_text += " "				
	return str(interpret_text)

def text1(button):
	desc1.set_text(interpret(lista_fenotipos[int(combo1.get_active())]))

def text2(button):
	desc2.set_text(interpret(lista_fenotipos[int(combo2.get_active())]))
	

def analyze_crosses(button):
	a = combo1.get_active()
	b = combo2.get_active()     
	if not a == -1 and not b == -1:
		result = logica.allPhenDec(lista_fenotipos[a],lista_fenotipos[b])
		resultados_resumen.set_buffer(texto1)
		resultados_completos.set_buffer(texto2)
		texto1.set_text(str(result[0]))  ### Poner aquí funcion con mejores resultados
		texto2.set_text(str(result[1])) #### Idem aca
		
import xml.etree.ElementTree as ET
from xml.dom import minidom


def save2XML(geneList,filename):
    # Este metodo salva la lista dada al archivo filename.
    root   = ET.Element("mendelianos")
    numgen = ET.SubElement(root,"numerodegenes",{"numero":str(len(geneList))})
    genes  = ET.SubElement(root,"genes")
    for k in range(len(geneList)):
        gen = ET.SubElement(genes, "gen", {"numero"   :str(k)        ,
                                           "dominante":geneList[k][0],
                                           "recesivo" :geneList[k][1],
                                           "domdescr" :geneList[k][2],
                                           "recdescr" :geneList[k][3]})
    rough    = ET.tostring(root)
    reparsed = minidom.parseString(rough)
    pretty   = reparsed.toprettyxml(indent="  ")
    root     = ET.fromstring(pretty)
    tree = ET.ElementTree(root)
    tree.write(filename)


def read4XML(filename):
    # Este metodo leee el archivo.
    geneList = []
    tree     = ET.parse(filename)
    root     = tree.getroot()
    for child in root:
        if child.tag == "genes":
            for grandchild in child:
                dominante = grandchild.attrib["dominante"]
                recesivo  = grandchild.attrib["recesivo"]
                domdescr  = grandchild.attrib["domdescr"]
                recdescr  = grandchild.attrib["recdescr"]
                geneList.append([dominante,recesivo,domdescr,recdescr])
    return geneList

#############################################


########################################Variables varias necesarias
Saved = False
texto1 = Gtk.TextBuffer() ## texto del resumen deberia ir aqui
texto2 = Gtk.TextBuffer() ## texto de resultados completos deberia ir aca
lista_alelos1 = Gtk.ListStore(str)
lista_alelos2 = Gtk.ListStore(str)
########################################

builder = Gtk.Builder()
render = Gtk.CellRendererText()
builder.add_from_file("proyecto.glade")

## handlers de cada evento


handlers={ 
	"terminar_app": Gtk.main_quit,
	"entry1check": enablebutton1,
	"entry2check": enablebutton2,
	"entry3check": enablebutton3,
	"entry4check": enablebutton4,
	"entry5check": enablebutton5,
	"entry6check": enablebutton6,
	"entrycorrect1": correcto_1,
	"entrycorrect2": correcto_2,
	"entrycorrect3": correcto_3,
	"entrycorrect4": correcto_4,
	"entrycorrect5": correcto_5,
	"entrycorrect6": correcto_6,
	"analyze": analyze_data,
	"pass_info": store_info,
	"analyze2_click": analyze_crosses,
	"save_button": save,
	"load_button": load,
	"text1":text1,
	"text2": text2
}

builder.connect_signals(handlers)

## Ventanas del programa

window = builder.get_object("ventana_principal")



################Llamamos a los objetos#############3

##Checks
check_1 = builder.get_object("checkbutton1")
check_2 = builder.get_object("checkbutton2")
check_3 = builder.get_object("checkbutton3")
check_4 = builder.get_object("checkbutton4")
check_5 = builder.get_object("checkbutton5")
check_6 = builder.get_object("checkbutton6")
##Letras
letra1 = builder.get_object("entry1dominantletter")
letra2 = builder.get_object("entry2dominantletter")
letra3 = builder.get_object("entry3dominantletter")
letra4 = builder.get_object("entry4dominantletter")
letra5 = builder.get_object("entry5dominantletter")
letra6 = builder.get_object("entry6dominantletter")

##Descripciones Dominantes
Ddescription1 = builder.get_object("entry1dominantdescription")
Ddescription2 = builder.get_object("entry2dominantdescription")
Ddescription3 = builder.get_object("entry3dominantdescription")
Ddescription4 = builder.get_object("entry4dominantdescription")
Ddescription5 = builder.get_object("entry5dominantdescription")
Ddescription6 = builder.get_object("entry6dominantdescription")
## Labels de las letras recesivas
Lrecesive1 =  builder.get_object("label1recesiveletter")
Lrecesive2 =  builder.get_object("label2recesiveletter")
Lrecesive3 =  builder.get_object("label3recesiveletter")
Lrecesive4 =  builder.get_object("label4recesiveletter")
Lrecesive5 =  builder.get_object("label5recesiveletter")
Lrecesive6 =  builder.get_object("label6recesiveletter")
##Descripciones recesivas
Rdescription1 = builder.get_object("entry1recesivedescription")
Rdescription2 = builder.get_object("entry2recesivedescription")
Rdescription3 = builder.get_object("entry3recesivedescription")
Rdescription4 = builder.get_object("entry4recesivedescription")
Rdescription5 = builder.get_object("entry5recesivedescription")
Rdescription6 = builder.get_object("entry6recesivedescription")

## Las listas de los alelos
combo1 = builder.get_object("combo1")
combo2 = builder.get_object("combo2")
Analyze_second = builder.get_object("Analyze_second")
##

resultados_resumen = builder.get_object("Resumen_resultados")
resultados_completos = builder.get_object("Resultados_completos")
##
desc1 = builder.get_object("desc1")
desc2 = builder.get_object("desc2")

filter_text = Gtk.FileFilter()
filter_text.set_name("Application / XML Files")
filter_text.add_mime_type("application/xml")


Lrecesive1.set_text("a")
render = Gtk.CellRendererText()
combo1.pack_start(render, True)
combo1.add_attribute(render, 'text', 0)
combo2.pack_start(render, True)
combo2.add_attribute(render, 'text', 0)
window.show_all()


Gtk.main()

