import sys
try:
	import gi
	gi.require_version('Gtk', '3.0')
	from gi.repository import Gtk, Gdk
except:
	print("GTK no disponible")
	sys.exit(1)


def numbify(widget):
	def filter_numbers(entry, *args):
		text = entry.get_text().strip()
		entry.set_text(''.join([i for i in text if i in '0123456789.']))
	widget.connect('changed', filter_numbers)

num_genes=0

class main:
	def __init__(self):
		#Creamos el builder
		self.builder = Gtk.Builder()
		self.builder.add_from_file("Chromosome_mapper3.glade")
		self.builder.connect_signals(self)
		
		#Setup de pantalla principal
		#Nombre de la ventana es Ventana_principal
		self.window = self.builder.get_object("Ventana_principal")
		self.window.set_title("Chromosome Mapper v0.1")
		
		#Setup del popup about
		self.about_window = self.builder.get_object("about_window")
		self.dialog_gen = self.builder.get_object("dialog_gen")

		#botones
		self.dialog_gen_ok = self.builder.get_object("dialog_gen_ok")	
		self.dialog_gen_cancel = self.builder.get_object("dialog_gen_cancel")	
		self.warning_label = self.builder.get_object("warning_label")


		#entradas
		self.gen_add_name = self.builder.get_object("gen_add_name")
		self.gen_add_description = self.builder.get_object("gen_add_description")
		self.gen_add_color = self.builder.get_object("gen_add_color")
		
		self.treeview = self.builder.get_object("treeview")

		#treeview
		self.store = Gtk.ListStore(str,str,str)
		self.treeview.set_model(self.store)

		self.gen_column = Gtk.TreeViewColumn('Gen')
		self.description_column = Gtk.TreeViewColumn('Descripción')
		self.color_column = Gtk.TreeViewColumn('Color')

		self.treeview.append_column(self.gen_column)
		self.treeview.append_column(self.description_column)
		self.treeview.append_column(self.color_column)

		self.cell = Gtk.CellRendererText()
		
		self.gen_column.pack_start(self.cell, True)
		self.description_column.pack_start(self.cell, True)
		self.color_column.pack_start(self.cell, True)

		self.gen_column.add_attribute(self.cell, 'text', 0)
		self.description_column.add_attribute(self.cell, 'text', 1)
		self.color_column.add_attribute(self.cell, 'text', 2)
		
		#Grid
		self.tabla = self.builder.get_object("grid_results")
			


		self.data_y = []
		self.data_x = []
		self.entry_matrix = []
		
		self.window.show()
		 
	def on_Ventana_principal_destroy(self,object,data=None):
		print("Quit")
		Gtk.main_quit()

	def on_menu_quit_activate(self,menuitem ,data=None):
		print("Quit")
		Gtk.main_quit()
	
	def on_menu_about_activate(self, menuitem, data=None):
		print('About')
		self.response = self.about_window.run()
		self.about_window.hide()
		print(self.response)

	def on_add_gene_activate(self,menuitem, data=None):
		print("Add Gene")
		self.gen_add_name.set_text("G"+ str(format(num_genes+1, '02d'))) ## Formato de numero
		self.response = self.dialog_gen.run()
		self.dialog_gen.hide()
		print(self.response)

	def on_dialog_gen_ok_clicked(self,button):
		print("OK")
		self.warning_label.set_text("")
		
		if self.gen_add_name.get_text() == "":
			self.warning_label.set_text("Debe escribir el nombre del gen")
		elif self.gen_add_description.get_text() == "":
			self.warning_label.set_text("Debe escribir la descripción del gen") ## agregar validacion de repetidos
		else:
			self.current_name = self.gen_add_name.get_text()
			self.current_description = self.gen_add_description.get_text()
			self.current_color = self.gen_add_color.get_rgba()

			self.store.append([self.current_name, self.current_description, self.current_color.to_string()])
			self.gen_add_name.set_text("")
			self.gen_add_description.set_text("")
			colorcolor = Gdk.RGBA()
			colorcolor.parse('#7F7F7F')
			self.gen_add_color.set_rgba(colorcolor)
			global num_genes
			num_genes +=1	
			self.dialog_gen.hide()
		
	
	def on_dialog_gen_cancel_clicked(self,button):
		self.current_name = ""
		self.current_description = ""
		self.current_color = ""
		self.warning_label.set_text("")
		self.gen_add_name.set_text("")
		self.gen_add_description.set_text("")
		colorcolor = Gdk.RGBA()
		colorcolor.parse('#7F7F7F')
		self.gen_add_color.set_rgba(colorcolor)
		print("cancel")
		self.dialog_gen.hide()

	def on_delete_gene_activate(self,menuitem, data=None):
		self.to_delete = self.treeview.get_selection()
		if  self.to_delete.get_selected()[1] == None:
			pass
		else:
			self.store.remove( self.to_delete.get_selected()[1])

	def numbify(widget):
		def filter_numbers(entry, *args):
			text = entry.get_text().strip()
			entry.set_text(''.join([i for i in text if i in '0123456789']))
		widget.connect('changed', filter_numbers)

	def on_populate_table_activate(self,menuitem, data = None):
		##Primero se destruye todo lo anterior para evitar errores
		if len(self.data_y) > 0:
			for i in range(len(self.data_y)):
				self.data_y[i].destroy()
					
			for i in range(len(self.data_x)):
				self.data_x[i].destroy()

			for i in range(len(self.entry_matrix)):
				for j in range(len(self.entry_matrix[i])):
					self.entry_matrix[i][j].destroy()
			
		self.label0=Gtk.Label()
		self.label0.set_text("*")
		self.tabla.attach(self.label0,0,0,1,1)
		self.data_y = []
		self.data_x = []
		self.entry_matrix = []  ### x,y
		
		self.label0.show()
		#print(self.builder.get_objects())
		for i,j in enumerate(self.store):
			self.data_y.append(Gtk.Label())
			self.tabla.attach(self.data_y[i],0,i+1,1,1)
			
			raw_name = str(j[:1])
			good_name = raw_name[2:-2]
			
			self.data_y[i].set_text(good_name)
			self.data_y[i].show()

		for i,j in enumerate(self.store):
			self.data_x.append(Gtk.Label())
			self.tabla.attach(self.data_x[i],i+1,0,1,1)

			raw_name = str(j[:1])
			good_name = raw_name[2:-2]

			self.data_x[i].set_text(good_name)
			self.data_x[i].show()

		for i in range(len(self.data_y)):
			temp_y=[]
			for j in range(len(self.data_y)):
				temp_y.append(Gtk.Entry())
				self.tabla.attach(temp_y[j],i+1,j+1,1,1)

				if i==j:
					temp_y[j].set_text("0")
					temp_y[j].set_editable(False)
				if j>i:
					temp_y[j].set_editable(False)
				if j<i:
					temp_y[j].set_editable(True)
					numbify(temp_y[j])

				temp_y[j].show()
			self.entry_matrix.append(temp_y)

	def on_Generar_mapa_activate(self,menuitem, data=None):
		print(format_the_data(symmetry_data(get_raw_data(self.entry_matrix))))

def get_raw_data(matriz): # saca los datos de los campos
	matriz_campos=[]	
	for i in range(len(matriz)):
		temp_i = []
		for j in range(len(matriz[i])):
			temp_i.append(matriz[i][j].get_text())
		matriz_campos.append(temp_i)
	return matriz_campos
			
				



#############################
def symmetry_data(data_matrix_input): ## da los reversos de lo que se colocó
	data_matrix = data_matrix_input
	for i in range(len(data_matrix)):
		for j in range(len(data_matrix[i])):
			if j>i:
				data_matrix[i][j] = data_matrix[j][i]
	return data_matrix

def clean_the_data(entry_array): #quita la linea de los labels a los datos recogidos
	clean_array = []
	for i in range(len(entry_array)):
		temporal_y = []
		for j in range(len(entry_array[i])):	
			if i!=0 and  j!=0:
				temporal_y.append(entry_array[i][j])
		clean_array.append(temporal_y)
		return_array = symmetry_data(clean_array)
	return return_array

def format_the_data(cleaned_array): # da los valores en float 
	formatted_array= []
	
	for i in range(len(cleaned_array)):
		temporal_y_format=[]
		for j in range(len(cleaned_array[i])):
			if cleaned_array[i][j]=="":
				temporal_y_format.append(float("NaN"))
			else :
				temporal_y_format.append(float(cleaned_array[i][j]))
		formatted_array.append(temporal_y_format)

	return formatted_array
	
	
				
		
			
			
x=float("NaN")		


main=main()

Gtk.main()