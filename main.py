from configparser import ConfigParser, DuplicateSectionError, NoOptionError, NoSectionError
from tkinter import Tk,Entry,Frame,Label,Button,LabelFrame,PhotoImage,Canvas, Menu, Toplevel, Scale, Checkbutton,IntVar,TclError
from tkinter import filedialog
from tkinter.ttk import Combobox,Scrollbar
from os.path import realpath,dirname,join
from sys import argv
from PIL import ImageTk,Image
import threading 
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import colors
CWD = dirname(argv[0])
SHOPPINGCART = ["#SHOPPING CART#"]
NAME = "YOUR NAME"
window = Tk()
window.geometry("740x500")
window.resizable(width=False, height=False)


# FINISH COLOR PICKER.

config = ConfigParser()

MainFrame = Frame(window,name="frame for all")
goodsFrame = Frame(MainFrame,name="frame for goods",bd=2,relief='groove',height=360,background="lightgrey")
secondFrame = Frame(MainFrame,name="second frame",bd=2,relief='groove',height=120,background="darkgrey")
buttonFrame = LabelFrame(secondFrame,name="frame for buttons",text="Funny buttons",bd=2,relief='groove',width=120)
cartFrame = LabelFrame(secondFrame,name="frame for shopping cart",text="Shopping Cart (Total: ​0₽)",bd=2,relief='groove',height=120)
cartFrameCanvas = Canvas(cartFrame)
cartFrameScrollbar = Scrollbar(cartFrame,orient="vertical",command=cartFrameCanvas.yview)
cartFrameCanvas.configure(yscrollcommand=cartFrameScrollbar.set)
cartFrameCanvas.bind("<Configure>",lambda e: cartFrameCanvas.config(scrollregion= cartFrameCanvas.bbox("all"))) 
cartFrameCanvasFrame = Frame(cartFrameCanvas)
cartFrameCanvas.create_window((0,0),window=cartFrameCanvasFrame, anchor="nw")

MainFrame.pack(fill="both",expand=1)
goodsFrame.pack(side='top',fill='both',expand=1,pady=20,padx=20)
secondFrame.pack(side='top',fill='both')
buttonFrame.pack(side="left",fill="y",padx=2, pady=2)
cartFrame.pack(side="top",anchor="ne",fill="x",padx=2, pady=2)

colorHexMode = IntVar(value=1)

class ColorPicker(Toplevel):
	def __init__(self, parent, *args):
		super().__init__(parent)
		self.topFrame = Frame(self,relief="groove",bg="darkgrey",bd=2)
		self.topFrame.pack(side="top",anchor="w")
		self.mainFrame = Frame(self.topFrame,relief="groove",bg="darkgrey",bd=2)
		self.mainFrame.pack(side="top",anchor="w",padx=20, pady=20)
		
		self.bottomFrame = Frame(self,relief="groove",bg="darkgrey",bd=2)
		self.bottomFrame.pack(side="top",anchor="w")
		self.colorPickFrame = Frame(self.bottomFrame,relief="groove",bd=2,bg="#ffffff")
		self.colorPickFrame.pack(side="left",anchor="n",padx=10, pady=10)
		self.colorFrame = Frame(self.bottomFrame,relief="groove",bd=2)
		self.colorFrame.pack(side="left",anchor="n",padx=10, pady=10)
		self.colorPickFavoritesFrame = Frame(self.colorFrame)
		self.colorPickFavoritesFrame.pack(side="bottom",anchor="w",padx=7, pady=5,ipadx=1,ipady=1)
		
		self.ColorLabels = []

		for row in range(0,4):
			favoriteColorFrame = Frame(self.colorPickFavoritesFrame,bg="#000000")
			favoriteColorFrame.pack(side="top",anchor="w",padx=4,pady=1)
			for column in range(0,5):
				favoriteColor = Label(favoriteColorFrame,width=10,height=2)
				favoriteColor.pack(side="left",padx=1,pady=1)
				favoriteColor.bind("<Button-1>",self.colorSetFuncGenerator(favoriteColor,favoriteColor))
				favoriteColor.bind("<Button-3>",self.colorGetFuncGenerator(favoriteColor))
				self.ColorLabels.append(favoriteColor)
		self.widgets = args
		
		self.redScale = Scale(self.colorFrame,from_=0.0,to=255.0,length=255,orient="vertical",command=self.colorChange)
		self.greenScale = Scale(self.colorFrame,from_=0.0,to=255.0,length=255,orient="vertical",command=self.colorChange)
		self.blueScale = Scale(self.colorFrame,from_=0.0,to=255.0,length=255,orient="vertical",command=self.colorChange)
		
		self.redScale.pack(side="right",anchor="n")
		self.greenScale.pack(side="right",anchor="n")
		self.blueScale.pack(side="right",anchor="n")

		self.colorLabel = Label(self.colorFrame,bg="black",width=35,height=10)
		self.colorLabel.pack(anchor="e",fill="both",expand=1)

		self.colorHexModeCheckbutton = Checkbutton(self.colorFrame,text="Enable HEX colornames",variable=colorHexMode,onvalue=1,offvalue=0, command=self.colorUpdateLabels)
		self.colorHexModeCheckbutton.pack(side="left",anchor="s")
		
		self.recursive(self.mainFrame,MainFrame)
		Lenght = int(len(colors.COLORS)**0.5)
		index = 0
		for row in range(1,Lenght):
			colorRow = Frame(self.colorPickFrame)
			colorRow.pack(side="top",anchor="w",pady=1)
			for column in range(1,Lenght):
				colorLabel = Label(colorRow,bg=colors.COLORS[index],width=2,height=1)
				colorLabel.bind("<Button-3>",self.colorGetFuncGenerator(colorLabel))
				colorLabel.pack(side="left",anchor="n",padx=1)
				index+=1
		

	def recursive(self, root, widget):
		for child in widget.winfo_children():
			childFrame = LabelFrame(root,text=child.winfo_name())
			if(widget.winfo_children().index(child)%2==0):
				childFrame.pack(side="left",anchor="n",pady=2,padx=2)
			else:
				childFrame.pack(side="right",anchor="n",pady=2,padx=2)
			try:child.cget("bg") # check if child has -bg option
			except TclError: # if not - print it's class
				print(child.winfo_class()) 
				childColorLabel = Label(childFrame, text="uncolorable")
			else:
				try:
					if(colorHexMode.get()==1): raise ValueError
					childColorLabel = Label(childFrame,text=",".join([str(int(child.cget("bg").lstrip('#')[n:n+2], 16)) for n in range(0, 6, 2)]), bg=child.cget("bg"))
				except ValueError:
					if("System" in child.cget("bg") or not "#" in child.cget("bg")):
						rgb = self._from_rgb(tuple((c//256 for c in child.winfo_rgb(child.cget("bg")))))
						childColorLabel = Label(childFrame,text=rgb,bg=child.cget("bg"))
						child.configure(bg=rgb)
					else:
						childColorLabel = Label(childFrame,text=str(child.cget("bg")), bg=child.cget("bg"))
			childColorLabel.pack(fill="x",expand=1,padx=2,pady=2)
			self.ColorLabels.append(childColorLabel)
			childColorLabel.bind("<Button-1>",self.colorSetFuncGenerator(child,childColorLabel))
			childColorLabel.bind("<Button-3>",self.colorGetFuncGenerator(child))
			childFrame
			self.recursive(childFrame,child)
	def colorSetFuncGenerator(self,widget,widgetCopy):
		def func(event):
			widget.configure(bg=self._from_rgb((self.redScale.get(),self.greenScale.get(),self.blueScale.get())))
			widgetCopy.configure(bg=self._from_rgb((self.redScale.get(),self.greenScale.get(),self.blueScale.get())))
			if(colorHexMode.get()==0):
				widgetCopy.configure(text=",".join([str(int(widgetCopy.cget("bg").lstrip('#')[n:n+2], 16)) for n in range(0, 6, 2)]))
			else:
				widgetCopy.configure(text=widgetCopy.cget("bg"))
		return func
	def colorGetFuncGenerator(self,widget):
		def func(event=None):
			try:
				rgb = tuple(int(widget.cget("bg").lstrip('#')[n:n+2], 16) for n in range(0, 6, 2))
				print(rgb)
				self.redScale.set(rgb[0])
				self.greenScale.set(rgb[1])
				self.blueScale.set(rgb[2])
			except ValueError: 
				rgb16bit = widget.winfo_rgb(widget.cget("bg"))
				rgb8bit = tuple((c//256 for c in rgb16bit))
				self.redScale.set(rgb8bit[0])
				self.greenScale.set(rgb8bit[1])
				self.blueScale.set(rgb8bit[2])
				return "#"+str(rgb8bit)
		return func
	def _from_rgb(self, rgb):
		#translates an rgb tuple of int to a tkinter friendly color code
		r, g, b = rgb
		return f'#{r:02x}{g:02x}{b:02x}'
	def colorChange(self,val):
		self.colorLabel.configure(bg=self._from_rgb((self.redScale.get(),self.greenScale.get(),self.blueScale.get())))
	def colorUpdateLabels(self):
		for label in self.ColorLabels:
			if label.cget("text")=="uncolorable":continue
			if(colorHexMode.get()==1):
				label.configure(text=self._from_rgb(tuple((c//256 for c in label.winfo_rgb(label.cget("bg"))))))
			else:
				try:label.configure(text=",".join([str(int(label.cget("bg").lstrip('#')[n:n+2], 16)) for n in range(0, 6, 2)]))
				except ValueError: 
					rgb8bit = ",".join(tuple((str(c//256) for c in label.winfo_rgb(label.cget("bg")))))
					label.configure(text=rgb8bit)
def openColorPicker():
	colorPickerWindow = ColorPicker(window, goodsFrame,secondFrame,buttonFrame,cartFrame)
	colorPickerWindow.grab_set()
	colorPickerWindow.resizable(width=False, height=False)
	return colorPickerWindow

menu = Menu()
menu.add_cascade(label="Color picker",command=openColorPicker)
window.config(menu=menu)
def telegramSend():
	global SHOPPINGCART
	text = ""
	for product in SHOPPINGCART:
		text = text + product + "\n\n"
	text = text + cartFrame["text"][cartFrame["text"].find("​")-8:]
	try:
		client = TelegramClient(StringSession(config.get("Telegram","Session")), ID, HASH)
	except (NoOptionError, ValueError):
		print(".ini HASH is wrong, using file")
		client = TelegramClient(NAME, ID, HASH)
		config.set("Telegram","Session",StringSession.save(client.session))
	client.connect()
	client.send_message("me",text)
	client.disconnect()
	print("Sent data")
	for widget in cartFrame.winfo_children():
		widget.destroy()
	SHOPPINGCART = ["#SHOPPING CART#"]
	cartFrame["text"] = "Shopping Cart (Total: ​0₽)"
telegramButton = Button(buttonFrame,text="Send list",command=telegramSend)

telegramButtonFlag = threading.Event()


def flagWait(flags, clear=True):
	try:
		done = False
		while not done:
			for flag in flags:
				if(flag.is_set()):
					if(clear):
						flag.clear()
					done = True
			window.update()
		
		
	except:
		quit()

class Product():
	def __init__(self,name:str,price:str,picture:str,location:str) -> None:
		self.name = name
		self.price = price
		self.picture = picture
		self.location = location 
		self.quantity = 0
		self.cost = 0
		self.label = Label()
		self.text = ""
	def add(self, arg=None):
		self.quantity = self.quantity+1
		previousCost = self.cost
		self.cost = int(self.quantity)*int(self.price)
		
		previousText = self.text
		self.text = "{} ({} units) @ {} for {}₽ each ({}₽ total)".format(self.name,self.quantity,self.location,self.price,self.cost)
		cartText = cartFrame["text"]
		cartIndex = cartText.find("​")
		if(self.quantity==1):
			SHOPPINGCART.append(self.text)
			self.label = Label(cartFrame,text=self.text,background="lightgrey") 
			self.label.pack(side="top",anchor="w")
			cartFrame["text"] = cartText[:cartIndex+1]+str(int(cartText[cartIndex+1:-2])+self.cost)+"₽)"
		else:
			index = SHOPPINGCART.index(previousText)
			SHOPPINGCART.pop(index)
			SHOPPINGCART.insert(index,self.text)
			self.label.configure(text=self.text)
			cartFrame["text"] = cartText[:cartIndex+1]+str(int(cartText[cartIndex+1:-2])-previousCost+self.cost)+"₽)"
	def remove(self):
		SHOPPINGCART.pop(SHOPPINGCART.index(self.text))
		self.label.destroy()
		cartText = cartFrame["text"]
		cartIndex = cartText.find("​")
		cartFrame["text"] = cartText[:cartIndex+1]+str(int(cartText[cartIndex+1:-2])-self.cost)+"₽)"
		self.quantity = 0
		self.cost = 0



def Main(SetupIncluded=False):
	products = config.sections()


	if(not SetupIncluded):
		productIndex = 0
		for productSection in products: # read all product-sections into product-objects
			if(productSection == "Telegram"):
				continue
			try:print(goodsFrame.winfo_children()[0])
			except:IndexError
			productFrame = Frame(goodsFrame,name = f"frame for product №{productIndex}",relief='groove',background='grey')
			productInfoFrame = Frame(productFrame,name = f"about product №{productIndex}",relief='groove',background='darkgrey')
			productInfoNameFrame = Frame(productInfoFrame,name = f"name of product №{productIndex}",relief='groove',background="darkgreen")
			productInfoMiscFrame = Frame(productInfoFrame,name = f"info about product №{productIndex}",relief='groove',background="lightgreen")
			
			product = Product(productSection,config.get(productSection,"price"),ImageTk.PhotoImage(Image.open(config.get(productSection,"picture")).resize((45,45),Image.NEAREST)),config.get(productSection,"location"))
			
			try: # if user did not selected any pic
				productPicFrame = Frame(productFrame,name=f"frame for pic №{productIndex}",bg="green")
				productPic = Label(productPicFrame,name=f"pic №{productIndex}",image=product.picture)
				productPic.image = product.picture
			except NameError:
				pass
			
			productLocation = Label(productInfoMiscFrame,name=f"location label №{productIndex}",text=product.location,font="Calibri 14")
			productPrice = Label(productInfoMiscFrame,name=f"price label №{productIndex}",text=product.price+"₽", font="Calibri 14" )
			productRemoveButton = Button(productFrame,name=f"remove button №{productIndex}",text="☓",command=product.remove)# change command to "remove"
			productNameLabel = Label(productInfoNameFrame,name=f"name label №{productIndex}",text=productSection,font="Calibri 14",bg="red")

			productFrame.pack(side="top",fill="x",pady=7,padx=7)
			productPicFrame.pack(side="left")
			productNameLabel.pack(side="left")
			productInfoNameFrame.pack(side="top",fill="x")
			productInfoMiscFrame.pack(side="bottom",fill="x")

			productPic.pack(side="left",padx=5,pady=5)
			productPic.bind("<Button-1>",product.add)
			productInfoFrame.pack(side="left",padx=10,fill="both",expand=1)
			productLocation.pack(side="left",padx=4)
			productPrice.pack(side="left")
			productRemoveButton.pack(side="right",fill="y")
			productIndex +=1
	telegramButton.pack(side="top",fill="x")
	window.mainloop()
	#while(True):
	#	window.update()

	# add functionality
def Setup():
	productIndex = 0
	# Flags that indicate that one iteration of setup routine is complete
	productFlag = threading.Event() 
	locationFlag = threading.Event()

	# Flags that indicate the completion of said setup routine
	locationsDoneFlag = threading.Event()
	productsDoneFlag = threading.Event()

	# List of location names
	locations = []
	
	# Frame and widgets for locations list setup
	setupLocationFrame = LabelFrame(goodsFrame,name=f"LabelFrame for location setup №{productIndex}",text="Enter name of location",bd=2,relief='groove',background='grey')
	setupLocationFrame.pack(side='top',anchor="nw",fill="x")
	setupLocationButton = Button(buttonFrame,name=f"Location setup 'done' button №{productIndex}",text="Done!",command=locationsDoneFlag.set)
	setupLocationButton.pack()

	LocationName = Entry(setupLocationFrame,name=f"Name of location entry №{productIndex}",width=50)
	LocationButton = Button(setupLocationFrame,name=f"Save button for location name №{productIndex}",text="save",command=locationFlag.set)
	LocationName.pack(side='left',padx=2)
	LocationButton.pack(side='left',padx=2)
	while True: # locations setup (Waits for user to hit "save", then saves this as new location)
		flagWait([locationFlag,locationsDoneFlag],clear=False)
		if(locationsDoneFlag.is_set()):
			setupLocationFrame.destroy()
			setupLocationButton.destroy()
			break
		else:
			locationFlag.clear()
		if(LocationName.get()==""):
			continue
		locations.append(LocationName.get())
		LocationName.delete(0,"end")

	
	# Frame and widgets for products setup
	setupProductFrame = LabelFrame(goodsFrame,name=f"setup frame for product №{productIndex}",text="Enter name of the product",bd=2,relief='groove',background='grey')
	setupProductFrame.pack(side='top',anchor="nw",fill="x")
	setupProductButton = Button(secondFrame,name=f"setup save button for all products №{productIndex}",text="Done!",command=productsDoneFlag.set) # button for finishing products setup
	setupProductButton.pack()

	setupProductName = Entry(setupProductFrame,name=f"entry setup for name of product №{productIndex}",width=50)
	setupProductName.pack(side='top',padx=2)

	productButton = Button(setupProductFrame,name=f"save button for all products in setup №{productIndex}",text="save",command=productFlag.set) # button for finishing iteration
	productButton.pack(side='left',padx=2)

	setupProductCombobox = Combobox(setupProductFrame,name=f"location combobox setup for product №{productIndex}",values=locations)
	setupProductCombobox.pack(side="left")

	setupProductPrice = Entry(setupProductFrame,name=f"price label setup for product №{productIndex}",width=24)
	setupProductPrice.pack(side="left")
	while True: # product setup
		global img # without making img global, python garbage collector will collect this image.
		global imgPath
		img = Image.new("RGB",[45,45],"white") # Create placeholder in case that user hasn't chosen an image
		img.save("placeholder.png")
		imgPath = open(realpath("placeholder.png")).name
		img = ImageTk.PhotoImage(Image.open(realpath("placeholder.png")))
		setupProductPic = Label(setupProductFrame,name=f"pic setup label №{productIndex}",text="Pick a pic!")
		setupProductPic.pack(side='left',padx=2)
		def pictureSelection(arg):
			global img
			global imgPath
			try:
				imgAtPath = filedialog.askopenfile(initialdir=CWD,mode="rb") # Opens file dialog
				imgPath = imgAtPath.name
				img = ImageTk.PhotoImage(Image.open(imgAtPath).resize((45,45),Image.NEAREST)) # Tries to load user's pic
			except AttributeError: pass # Skips if they didn't chose anything
			setupProductPic.configure(image=img,text="")
		setupProductPic.bind("<Button-1>",pictureSelection)

		flagWait([productFlag,productsDoneFlag],clear=False)
		if(productsDoneFlag.is_set()):
			setupProductFrame.destroy() # cleaning setup-related stuff, if user is done
			setupProductButton.destroy()
			with open(join(CWD,'settings','test.ini'), 'w', encoding="UTF-8") as configfile:
				config.write(configfile)
			break
		else: # and if they aren't, do a bunch of things
			productFlag.clear()
			# combining all data in one place and, most importantly, unbounding it from setup-variables
			
			# creating new frame
			productFrame = LabelFrame(goodsFrame,name=f"labelframe for product №{productIndex}",text=product.name,relief='groove',background='grey')
			
			product = Product(
				setupProductName.get(),
				setupProductPrice.get(),
				img,
				setupProductCombobox.get()
			)
			iteration = 1
			while(True): # this thing uses invisible character u/200b trying to locate copy tag at the end
				try:
					config.add_section(product.name)
					break
				except DuplicateSectionError:
					if(iteration == 1):
						product.name = product.name +"​("+str(iteration)+")"
						iteration+=1
						continue					
					indexNumberOfCopies = product.name.find("​")
					product.name = product.name[:indexNumberOfCopies] + "​("+str(int(product.name[indexNumberOfCopies+2:-1])+1)+")"
					iteration+=1
			config.set(product.name,"picture",imgPath)
			config.set(product.name,"price",product.price)
			config.set(product.name,"location",product.location)

			
			try: # if user did not selected any pic
				productPic = Label(productFrame,name=f"pic of product №{productIndex}",image=product.picture)
				productPic.image = product.picture
			except NameError:
				setupProductPic.destroy() #clean previous picture you've selected
				continue

			productLocation = Label(productFrame,name=f"location label for product №{productIndex}",text="Location: "+product.location)
			productPrice = Label(productFrame,name=f"price label of product №{productIndex}",text="Price (₽): "+product.price )
			productAddButton = Button(productFrame,text=f"Add to cart №{productIndex}") # this button should not exist
			

			productFrame.pack(side="bottom",fill="x")
			productPic.pack(side="left")
			productLocation.pack(side="left",padx=4)
			productPrice.pack(side="left")
			productAddButton.pack(side="right")

			#cleaning
			setupProductPic.destroy()
			setupProductName.delete(0,"end")
			setupProductPrice.delete(0,"end")

			productIndex +=1
		window.update()
	window.update()	
	Main(SetupIncluded=True)
config.read(join(CWD,'settings','test.ini'), encoding="UTF-8")
try:
	ID = config.get("Telegram","ID")
	HASH = config.get("Telegram","HASH")
except NoSectionError:
	config.add_section("Telegram")
	print("No .ini credentials section. Input ID")
	ID = input()
	config.set("Telegram","ID","%s"%ID)
	print("Input HASH")
	HASH = input()
	config.set("Telegram","HASH","%s"%HASH)
except NoOptionError:
	print(".ini credentials are corrupted or non-existand. Enter ID")
	ID = input()
	config.set("Telegram","ID","%s"%ID)
	print("Input HASH")
	HASH = input()
	config.set("Telegram","HASH","%s"%HASH)
try:
	if(config.sections()!=["Telegram"]):
		Main(SetupIncluded=False)
	else:
		open(join(CWD,'settings','test.ini'),"w")
		config.read(join(CWD,'settings','test.ini'), encoding="UTF-8")
		Setup()
except KeyboardInterrupt:
	print("ctrl+c quit")
	quit()

########################################
############# NOT FINISHED ################
	"""
		1. Pages
		2. "Edit" button
		3. Unpolished design 
		4. Accurate product data
		5. Fix perfomance issues
		6. Pack everything
	"""
############# NOT FINISHED ################
########################################