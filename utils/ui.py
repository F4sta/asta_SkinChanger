import dearpygui.dearpygui as dpg
import json
import ctypes
user32 = ctypes.windll.user32
screenwidth, screenheight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
from utils.helper import *
from time import sleep
from configparser import ConfigParser
import pymem

c = ConfigParser()
while True:
    try:
        with open("utils/skin_dict.json", "r", encoding="utf-8") as file:
            Skin_dict = dict(json.load(file))
            break
    except:
        continue
reverse_skin_dict = {v: k for k, v in Skin_dict.items()}
skin_names = list(Skin_dict.keys())
skin_IDs = list(Skin_dict.values())
temp_skinnames = skin_names
WEAPONS = ["ak47","m4a4","m4a1s","galiar","famas","awp","ssg08",
        "usp","glock","deagle","p250","fiveseven","tec9","revolver"]

''' Handle Paintkits functions '''
def getIdByPaintkit(paintkit):
    return Skin_dict[paintkit]

def getPaintkitById(Id):
    return reverse_skin_dict[f"{Id}"]

#Default Variables
DEF_WEAPON = WEAPONS[0]
DEF_PAINTID = skin_IDs[0]
DEF_FLOAT = 0.000001
DEF_SEED = 0
DEF_STATTRAK = False
DEF_STATTRAK_VALUE = 1
DEF_CONFIGFILE = "Config1"
#Current Variables
cur_configfile = DEF_CONFIGFILE
cur_weapon = DEF_WEAPON
cur_paintID = DEF_PAINTID
cur_paintkit = getPaintkitById(DEF_PAINTID)
cur_float = DEF_FLOAT
cur_seed = DEF_SEED
cur_stattrak = DEF_STATTRAK
cur_stattrak_value = DEF_STATTRAK_VALUE

''' Config functions '''

def updateConfig():
    global cur_paintkit, cur_float, cur_seed,cur_stattrak, cur_stattrak_value, cur_paintID
    with open("Config/current_config.txt") as file:
        cur_configfile = file.readline()
        c.read(f"Config/{cur_configfile}.ini")
        #Weapon Config
        cur_paintID = int(c["Skins"][cur_weapon])
        Float = float(c["Float"][cur_weapon])
        if 0 >= Float >= 1:
            Float = 0.0000001
        Seed = int(c["Seed"][cur_weapon])
        Stattrak = BoolenConfig(c["Stattrak"][cur_weapon])
        Stattrak_value = int(c["StattrakValue"][cur_weapon])
        if 0 >= Stattrak_value >= 1000000:
            Stattrak_value = 69
        
        cur_paintkit = getPaintkitById(cur_paintID)
        cur_float = Float
        cur_seed = Seed
        cur_stattrak = Stattrak
        cur_stattrak_value = Stattrak_value

def saveConfig():
    global cur_weapon
    #Weapon Config
    c["Skins"][cur_weapon] = str(getIdByPaintkit(dpg.get_value("paintkit_value")))
    float_ = dpg.get_value("Float_value")
    float_ = "{:.6f}".format(float_)
    if float_ == "1e-06":
        float_ = "0.000001"
    c["Float"][cur_weapon] = str(float_)
    c["Seed"][cur_weapon] = str(dpg.get_value("seed_value"))
    c["Stattrak"][cur_weapon] = str(dpg.get_value("stattrak_bool"))
    c["StattrakValue"][cur_weapon] = str(dpg.get_value("stattrak_value"))
        
    with open(f"Config/{cur_configfile}.ini", "w", encoding="utf-8") as file:
        c.write(file)

def setValues():
    global cur_paintID, cur_float, cur_seed, cur_stattrak, cur_stattrak_value, cur_paintkit
    updateConfig()
    dpg.set_value("paintkit_search", cur_paintkit)
    dpg.set_value("paintkit_value", cur_paintkit)
    dpg.set_value("Float_value", cur_float)
    dpg.set_value("seed_value", cur_seed)
    dpg.set_value("stattrak_bool", cur_stattrak)
    dpg.set_value("stattrak_value", cur_stattrak_value)

''' Callbacks functions '''
def currentWeaponCallback(Sender):
    global cur_weapon, cur_configfile
    weapon = str(dpg.get_value(Sender))
    cur_weapon = weapon
    setValues()

def paintkit_input_callback():
    paintkit_input = str(dpg.get_value("paintkit_search"))
    if paintkit_input != "":
        temp_skinnames = [] 
        for i in skin_names:
            if paintkit_input.lower() in str(i).lower():
                temp_skinnames.append(i)
            if i == skin_names[-1]:
                dpg.configure_item("paintkit_value", items=temp_skinnames)
    else:
        temp_skinnames = skin_names
        dpg.configure_item("paintkit_value", items=temp_skinnames)
    saveConfig()

def ChangeConfig(NextPrev : str):
    global cur_configfile
    Continue = True
    index = cur_configfile[-1]
    if NextPrev == "Next":
        if index == "9":
            Continue = False
        else:
            index = int(index) + 1
            Continue = True
    elif NextPrev == "Prev":
        if index == "1":
            Continue = False
        else:
            index = int(index) - 1
            Continue = True
    if Continue:
        cur_configfile = "Config" + str(index)
        with open("Config/current_config.txt", "w") as file:
            file.write(cur_configfile)
        dpg.set_value("config_text", f"Config: {cur_configfile}")
        setValues()
        paintkit_input_callback()
        

def clearAllConfig():
    for i in range(1, 10):
        with open("Config/DefaultConfig.ini", "r") as def_file:
            fileName = f"Config/Config{i}.ini"
            with open(fileName, "w") as file:
                file.write(def_file.read())
    setValues()
                
def clearConfig(id):
    with open("Config/DefaultConfig.ini", "r") as def_file:
        fileName = f"Config/Config{id}.ini"
        with open(fileName, "w") as file:
            file.write(def_file.read())
    setValues()


''' Main function '''
def main():
    updateConfig()
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()
    
    ICON="Images/logo.ico"

    with dpg.window(label="Main", tag="Main"):
        
        WIDTH, HEIGHT = 500, 350
        #Setting the main window
        dpg.set_primary_window("Main", True)
        dpg.set_viewport_max_width(WIDTH)
        dpg.set_viewport_max_height(HEIGHT)
        dpg.set_viewport_pos([(screenwidth/2-WIDTH), (screenheight/2-HEIGHT)])
        dpg.set_viewport_resizable(False)
        dpg.set_viewport_title("asta's Skinschanger")
        dpg.set_viewport_large_icon(ICON)
        dpg.set_viewport_small_icon(ICON)
        
        with dpg.tab_bar(tag="MainTab"):
            with dpg.tab(label="Rifles"):
                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    with dpg.table_row():
                        with dpg.table(header_row=False):
                            dpg.add_table_column()

                            with dpg.table_row():dpg.add_combo(tag="WEAPONS", items=WEAPONS, default_value=cur_weapon,
                                                    callback=currentWeaponCallback,
                                                    width=100)
                                
                            #Float Input
                            with dpg.table_row():dpg.add_text("Float")
                            with dpg.table_row():
                                dpg.add_input_float(tag="Float_value", min_value=0.000001, max_value=0.999999,
                                                    step=0.1, min_clamped=True, max_clamped=True,
                                                    format='%.6f', default_value=cur_seed,
                                                    callback=saveConfig,
                                                    width=220)
                                
                            #Seed Input
                            with dpg.table_row():dpg.add_text("Seed")
                            with dpg.table_row():dpg.add_input_int(tag="seed_value", max_value=1000, min_value=0,
                                                    max_clamped=True, min_clamped=True, default_value=cur_seed,
                                                    callback=saveConfig,
                                                    width=220)
                                
                            
                            #Stattrak Input
                            with dpg.table_row():dpg.add_checkbox(tag="stattrak_bool", label="StatTrak", default_value=cur_stattrak,
                                                    callback=saveConfig)
                            with dpg.table_row():dpg.add_input_int(tag="stattrak_value", max_value=999999, min_value=1,
                                                    max_clamped=True, min_clamped=True, default_value=cur_stattrak_value,
                                                    callback=saveConfig,
                                                    width=220)
                            
                            with dpg.table_row():dpg.add_spacer(height=52)
                            with dpg.table_row():dpg.add_text(f"Config: {cur_configfile}", tag="config_text")
                            with dpg.table_row():
                                with dpg.table(header_row=False):
                                    dpg.add_table_column()
                                    dpg.add_table_column()
                                    with dpg.table_row():
                                        dpg.add_button(label="Previous", width=100, callback=lambda : ChangeConfig("Prev"))
                                        dpg.add_button(label="Next", width=100, callback=lambda : ChangeConfig("Next"))
                                
                        
                        with dpg.table(header_row=False):
                            dpg.add_table_column()
                            with dpg.table_row():dpg.add_text("Paintkits")
                            with dpg.table_row():
                                with dpg.table(header_row=False):
                                    dpg.add_table_column(width=20, width_fixed=True)
                                    dpg.add_table_column(width=210, width_stretch=True)
                                    with dpg.table_row():
                                        dpg.add_text("Seachbar: ")
                                        dpg.add_input_text(tag="paintkit_search", callback=paintkit_input_callback, width=210)
                                        
                            with dpg.table_row():dpg.add_listbox(tag="paintkit_value", items=skin_names, default_value=cur_paintkit,
                                                    callback=saveConfig, num_items=12, width=230)
                
            with dpg.tab(label="Settings"):
                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    with dpg.table_row():
                        
                        with dpg.table(header_row=False):
                            dpg.add_table_column()
                            with dpg.table_row():dpg.add_text("Config")
                            with dpg.table_row():dpg.add_separator()
                            with dpg.table_row():dpg.add_button(label="Clear Current Config", callback=lambda: clearConfig(cur_configfile[-1]))
                            with dpg.table_row():dpg.add_button(label="Clear All Config", callback=clearAllConfig)

    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 16, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 3, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 3, category=dpg.mvThemeCat_Core)
            
    setValues()
    dpg.bind_theme(global_theme)
    dpg.show_viewport()
    while dpg.is_dearpygui_running():
        sleep(0.02)
        updateConfig()
        dpg.render_dearpygui_frame()
    dpg.destroy_context()

if __name__ == '__main__':
    main()
    