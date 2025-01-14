import armor_stand_geo_class
import armor_stand_class
import structure_reader
import animation_class
import render_controller_class as rcc
from tkinter import StringVar, Button, Label, Entry, Tk, Checkbutton, END, ACTIVE
from tkinter import filedialog, Scale,DoubleVar,HORIZONTAL,IntVar,Listbox, ANCHOR
import manifest
from shutil import copyfile
import os
from zipfile import ZipFile
import glob
import shutil
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

def process_block(x,y,z,block):
    rot = None
    top = False
    open_bit = False
    ## everything below is handling the garbage mapping and naming in NBT
    ## probably should be cleaned up into a helper function/library. for now it works-ish
    variant="Default"
    if "wall_block_type" in block["states"].keys():
        variant = ["wall_block_type",block["states"]["wall_block_type"]]
    if "wood_type" in block["states"].keys():
        variant = ["wood_type",block["states"]["wood_type"]]
        if block["name"] == "minecraft:wood":
            keys = block["states"]["wood_type"]
            if bool(block["states"]["stripped_bit"]):
                keys+="_stripped"
            variant = ["wood",keys]
    if "old_log_type" in block["states"].keys():
        variant = ["old_log_type",block["states"]["old_log_type"]]
    if "new_log_type" in block["states"].keys():
        variant = ["new_log_type",block["states"]["new_log_type"]]
    if "stone_type" in block["states"].keys():
        variant = ["stone_type",block["states"]["stone_type"]]
    if "prismarine_block_type" in block["states"].keys():
        variant = ["prismarine_block_type",block["states"]["prismarine_block_type"]]
    if "stone_brick_type" in block["states"].keys():
        variant = ["stone_brick_type",block["states"]["stone_brick_type"]]
    if "color" in block["states"].keys():
        variant = ["color",block["states"]["color"]]
    if "sand_stone_type" in block["states"].keys():
        variant = ["sand_stone_type",block["states"]["sand_stone_type"]]
    if "stone_slab_type" in block["states"].keys():
        variant = ["stone_slab_type",block["states"]["stone_slab_type"]]
    if "stone_slab_type_2" in block["states"].keys():
        variant = ["stone_slab_type_2",block["states"]["stone_slab_type_2"]]
    if "stone_slab_type_3" in block["states"].keys():
        variant = ["stone_slab_type_3",block["states"]["stone_slab_type_3"]]
    if "stone_slab_type_4" in block["states"].keys():
        variant = ["stone_slab_type_4",block["states"]["stone_slab_type_4"]]
    if "facing_direction" in block["states"].keys():
        rot = block["states"]["facing_direction"]
    if "direction" in block["states"].keys():
        rot = block["states"]["direction"]
    if "top_slot_bit" in block["states"].keys():
        top = bool(block["states"]["top_slot_bit"])
    if "weirdo_direction" in block["states"].keys():
        rot = int(block["states"]["weirdo_direction"])
    if "upside_down_bit" in block["states"].keys():
        top = bool(block["states"]["upside_down_bit"])
    if "open_bit" in block["states"].keys():
        open_bit = bool(block["states"]["open_bit"])
    return [rot, top, variant, open_bit]
def generate_pack(struct_name, pack_name,opacity):
    visual_name=pack_name
    pack_name=pack_name.replace(" ","_")
    # check that the pack name is not already used
    global models, offsets
    if check_var.get()==0:
        model_name=""
        offsets={"":[xvar.get(),yvar.get(),zvar.get()]}
        models={"":struct_name}
    else:
        fileName="{} Nametags.txt".format(pack_name)
        with open(fileName,"w+") as text_file:
            text_file.write("These are the nametags used in this file\n")
            for name in models.keys():
                text_file.write("{}\n".format(name))
        
    while os.path.isfile("{}.mcpack".format(pack_name)) or pack_name == "":
        pack_name = filedialog.asksaveasfilename(initialdir = os.getcwd(),
                                                 title = "Select a New Name",
                                                 filetypes = (("pack files",
                                                               "*.mcpack"),
                                                              ("all files",
                                                               "*.*")))
        
        pack_name=ntpath.basename(pack_name)
    ## makes a render controller class that we will use to hide models
    rc=rcc.render_controller()
    ##makes a armor stand entity class that we will use to add models 
    armorstand_entity = armor_stand_class.armorstand()
    ##manifest is mostly hard coded in this function.
    manifest.export(visual_name)
    
    ## repeate for each structure after you get it to work
    #creats a base animation controller for us to put pose changes into
    animation = animation_class.animations()
    longestY=0
    update_animation=True
    for model_name in models.keys():
        offset=offsets[model_name]
        rc.add_model(model_name)
        armorstand_entity.add_model(model_name)
        copyfile(models[model_name], "{}/{}.mcstructure".format(pack_name,model_name))
        
        #reads structure
        struct2make = structure_reader.process_structure(models[model_name])
        #creates a base armorstand class for us to insert blocks
        armorstand = armor_stand_geo_class.armorstandgeo(model_name,alpha = opacity,offsets=offset)
        
        #gets the shape for looping
        [xlen, ylen, zlen] = struct2make.get_size()
        if ylen > longestY:
            update_animation=True
            longestY = ylen
        else:
            update_animation=False
        for y in range(ylen):
            #creates the layer for controlling. Note there is implied formating here
            #for layer names
            armorstand.make_layer(y)
            #adds links the layer name to an animation
            if update_animation:
                animation.insert_layer(y)
            for x in range(xlen):
                for z in range(zlen):
                    #gets block
                    block = struct2make.get_block(x, y, z)
                    blk_name=block["name"].replace("minecraft:", "")
                    [rot, top, variant, open_bit]=process_block(x,y,z,block)
                    ##  If java worlds are brought into bedrock the tools some times
                    ##   output unsupported blocks, will log.
                    
                    try:
                        armorstand.make_block(x, y, z, blk_name, rot = rot, top = top,variant = variant, trap_open=open_bit)
                    except:
                        print("There is an unsuported block in this world and it was skipped")
                        print("x:{} Y:{} Z:{}, Block:{}, Variant: {}".format(x,y,z,block["name"],variant))
        ## this is a quick hack to get block lists, doesnt consider vairants.... so be careful                
        allBlocks = struct2make.get_block_list()
        fileName="{}-{} block list.txt".format(visual_name,model_name)
        if export_list.get()==1:
            with open(fileName,"w+") as text_file:
                text_file.write("This is a list of blocks, there is a known issue with variants, all variants are counted together\n")
                for name in allBlocks.keys():
                    commonName = name.replace("minecraft:","")
                    text_file.write("{}: {}\n".format(commonName,allBlocks[name]))
        
        # call export fuctions
        armorstand.export(pack_name)
        animation.export(pack_name)

        ##export the armorstand class
        armorstand_entity.export(pack_name)
        
    # Copy my icons in
    copyfile("lookups/pack_icon.png", "{}/pack_icon.png".format(pack_name))
    # Adds to zip file a modified armor stand geometry to enlarge the render area of the entity
    larger_render = "lookups/armor_stand.larger_render.geo.json"
    larger_render_path = "{}/models/entity/{}".format(pack_name, "armor_stand.larger_render.geo.json")
    copyfile(larger_render, larger_render_path)
    # the base render controller is hard coded and just copied in
        
        
    rc.export(pack_name)
    ## get all files
    file_paths = []
    for directory,_,_ in os.walk(pack_name):
        file_paths.extend(glob.glob(os.path.join(directory, "*.*")))
    
    ## add all files to the mcpack file  
    with ZipFile("{}.mcpack".format(pack_name), 'x') as zip: 
        # writing each file one by one 

        for file in file_paths:
            print(file)
            zip.write(file)
    ## delete all the extra files.
    shutil.rmtree(pack_name)


def runFromGui():
    ##wrapper for a gui.
    stop = False
    if check_var.get()==0:
        if len(FileGUI.get()) == 0:
            stop = True
            messagebox.showinfo("Error", "You need to browse for a structure file!")
        if len(packName.get()) == 0:
            stop = True
            messagebox.showinfo("Error", "You need a Name")
    else:
        if len(list(models.keys()))==0:
            stop = True
            messagebox.showinfo("Error", "You need to add some strucutres")
            
    opacity=(100-sliderVar.get())/100
    
    if not stop:
        generate_pack(FileGUI.get(), packName.get(),opacity)


def browseStruct():
    #browse for a structure file.
    FileGUI.set(filedialog.askopenfilename(filetypes=(
        ("Structure File", "*.mcstructure *.MCSTRUCTURE"), )))

def box_checked():
    if check_var.get()==0:
        modle_name_entry.grid_forget()
        modle_name_lb.grid_forget()
        deleteButton.grid_forget()
        listbox.grid_forget()
        saveButton.grid_forget()
        modelButton.grid_forget()
        r = 0
        file_lb.grid(row=r, column=0)
        file_entry.grid(row=r, column=1)
        packButton.grid(row=r, column=2)
        r += 1
        packName_lb.grid(row=r, column=0)
        packName_entry.grid(row=r, column=1)
        r += 1
        cord_lb.grid_forget()
        x_entry.grid_forget()
        y_entry.grid_forget()
        z_entry.grid_forget()
        transparency_lb.grid_forget()
        transparency_entry.grid_forget()
        advanced_check.grid(row=r, column=0)
        export_check.grid(row=r, column=1)
        saveButton.grid(row=r, column=2)
    else:
        saveButton.grid_forget()
        r = 0
        file_lb.grid(row=r, column=0)
        file_entry.grid(row=r, column=1)
        packButton.grid(row=r, column=2)
        r += 1
        packName_lb.grid(row=r, column=0)
        packName_entry.grid(row=r, column=1)
        r += 1
        modle_name_entry.grid(row=r, column=1)
        modle_name_lb.grid(row=r, column=0)
        modelButton.grid(row=r, column=2)
        r += 1
        cord_lb.grid(row=r, column=0,columnspan=3)
        r += 1
        x_entry.grid(row=r, column=0)
        y_entry.grid(row=r, column=1)
        z_entry.grid(row=r, column=2)
        r += 1
        transparency_lb.grid(row=r, column=0)
        transparency_entry.grid(row=r, column=1,columnspan=2)
        r += 1
        listbox.grid(row=r,column=1, rowspan=3)
        deleteButton.grid(row=r,column=2)
        r += 4
        advanced_check.grid(row=r, column=0)
        export_check.grid(row=r, column=1)
        saveButton.grid(row=r, column=2)
def add_model():
    valid=True
    if len(FileGUI.get()) == 0:
        valid=False
        messagebox.showinfo("Error", "You need to browse for a structure file!")
    if len(model_name_var.get()) == 0:
        valid=False
        messagebox.showinfo("Error", "You need a name for the Name Tag!")
    if model_name_var.get() in list(models.keys()):
        messagebox.showinfo("Error", "The Name Tag mut be unique")
        valid=False
    if valid:
        
        listbox.insert(END,model_name_var.get())
        offsets[model_name_var.get()]=[xvar.get(),yvar.get(),zvar.get()]
        models[model_name_var.get()]=FileGUI.get()
def delete_model():
    items = listbox.curselection()
    if len(items)>0:
        models.pop(listbox.get(ACTIVE))
    listbox.delete(ANCHOR)
offsets={}
root = Tk()
root.title("Structura")
models={}
FileGUI = StringVar()
packName = StringVar()
sliderVar = DoubleVar()
model_name_var = StringVar()
xvar = DoubleVar()
xvar.set(8)
yvar = DoubleVar()
zvar = DoubleVar()
zvar.set(7)
check_var = IntVar()
export_list = IntVar()
sliderVar.set(20)
listbox=Listbox(root)
file_entry = Entry(root, textvariable=FileGUI)
packName_entry = Entry(root, textvariable=packName)
modle_name_lb = Label(root, text="Name Tag")
modle_name_entry = Entry(root, textvariable=model_name_var)
cord_lb = Label(root, text="offset")
x_entry = Entry(root, textvariable=xvar, width=5)
y_entry = Entry(root, textvariable=yvar, width=5)
z_entry = Entry(root, textvariable=zvar, width=5)
file_lb = Label(root, text="Structure file")
packName_lb = Label(root, text="Pack Name")
packButton = Button(root, text="Browse", command=browseStruct)
advanced_check = Checkbutton(root, text="advanced", variable=check_var, onvalue=1, offvalue=0, command=box_checked)
export_check = Checkbutton(root, text="make lists", variable=export_list, onvalue=1, offvalue=0)

deleteButton = Button(root, text="Remove Model", command=delete_model)
saveButton = Button(root, text="Make Pack", command=runFromGui)
modelButton = Button(root, text="Add Model", command=add_model)

transparency_lb = Label(root, text="Transparency")
transparency_entry = Scale(root,variable=sliderVar, length=200, from_=0, to=100,tickinterval=10,orient=HORIZONTAL)

box_checked()

root.mainloop()
root.quit()
