import dearpygui.dearpygui as dpg
import json
import ctypes
user32 = ctypes.windll.user32
screenwidth, screenheight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
from helper import *
from time import sleep
from configparser import ConfigParser
import pymem
from offsets import dwClientState

''' csgo_initialize  =  False
while not csgo_initialize:
    try:
        pm = pymem.Pymem( "csgo.exe" )
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
        engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
        csgo_initialize  =  True
    except:
        continue '''

c = ConfigParser()
with open("skin_dict.json", "r", encoding="utf-8") as file:
    Skin_dict = dict(json.load(file))
reverse_skin_dict = {v: k for k, v in Skin_dict.items()}
skin_names = list(Skin_dict.keys())
temp_skinnames = skin_names
WEAPONS = ["ak47","m4a4","m4a1s","galiar","famas","awp","ssg08",
        "usp","glock","deagle","p250","fiveseven","tec9","revolver"]

#Default Variables
DEF_WEAPON = WEAPONS[0]
DEF_PAINT = skin_names[0]
DEF_FLOAT = 0.000001
DEF_SEED = 0
DEF_STATTRAK = False
DEF_STATTRAK_VALUE = 1
DEF_CONFIGFILE = "Config1"
#Current Variables
cur_configfile = DEF_CONFIGFILE
curweapon = DEF_WEAPON
cur_paintkit = DEF_PAINT
cur_float = DEF_FLOAT
cur_seed = DEF_SEED
cur_stattrak = DEF_STATTRAK
cur_stattrak_value = DEF_STATTRAK_VALUE

''' Config functions '''

def getConfig():
    global cur_configfile
    with open("Config/current_config.txt") as file:
        cur_configfile = file.readline()
        c.read(f"Config/{cur_configfile}.ini")
    

def saveConfig():
    print("saveConfig called")
    global curweapon
    with open("Config/current_config.txt") as file:
        cur_configfile = file.readline()
    
    #Weapon Config
    c["Skins"][curweapon] = str(getIdByPaintkit(dpg.get_value("paintkit_value")))
    float_ = dpg.get_value("Float_value")
    float_ = "{:.6f}".format(float_)
    if float_ == "1e-06":
        float_ = "0.000001"
    c["Float"][curweapon] = str(float_)
    c["Seed"][curweapon] = str(dpg.get_value("seed_value"))
    c["Stattrak"][curweapon] = str(dpg.get_value("stattrak_bool"))
    c["StattrakValue"][curweapon] = str(dpg.get_value("stattrak_value"))
        
    with open(f"Config/{cur_configfile}.ini", "w", encoding="utf-8") as file:
        c.write(file)


''' Handle Paintkits functions '''
def getIdByPaintkit(paintkit):
    return Skin_dict[paintkit]

def getPaintkitById(Id):
    return reverse_skin_dict[f"{Id}"]

''' Callbacks functions '''
def currentWeaponCallback(Sender):
    global curweapon, cur_paintkit, cur_float, cur_seed,cur_stattrak, cur_stattrak_value, cur_configfile
    weapon = str(dpg.get_value(Sender))
    curweapon = weapon
    
    c.read(f"Config/{cur_configfile}.ini")
    
    #Weapon Config
    paint = int(c["Skins"][weapon])
    Float = float(c["Float"][weapon])
    if 0 >= Float >= 1:
        Float = 0.0000001
    Seed = int(c["Seed"][weapon])
    Stattrak = BoolenConfig(c["Stattrak"][weapon])
    Stattrak_value = int(c["StattrakValue"][weapon])
    if 0 >= Stattrak_value >= 1000000:
        Stattrak_value = 69
    
    cur_paintkit, cur_float, cur_seed, cur_stattrak, cur_stattrak_value = paint, Float, Seed, Stattrak, Stattrak_value
    
    
    dpg.set_value("paintkit_seach", "")
    dpg.set_value("paintkit_value", getPaintkitById(cur_paintkit))
    dpg.set_value("Float_value", cur_float)
    dpg.set_value("seed_value", cur_seed)
    dpg.set_value("stattrak_bool", cur_stattrak)
    dpg.set_value("stattrak_value", cur_stattrak_value)

def paintkit_input_callback(Sender):
    paintkit_input = str(dpg.get_value(Sender))
    if not paintkit_input == "":
        temp_skinnames = [] 
        for i in skin_names:
            if paintkit_input.lower() in str(i).lower():
                temp_skinnames.append(i)
            if i == skin_names[-1]:
                dpg.configure_item("paintkit_value", items=temp_skinnames)
    else:
        temp_skinnames = skin_names;dpg.configure_item("paintkit_value", items=temp_skinnames)
    
def forceUpdate():
    ''' 
    try:
        pm.write_int(pm.read_uint( engine + dwClientState ) + 0x174, -1)
    except:
        print("Cant Update Skinchanger") '''
    pass

''' Main function '''
def main():
    getConfig()
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()
    
    ICON="Images/logo.ico"

    with dpg.window(label="Main", tag="Main", width=500, height=350):
        
        #Setting the main window
        #dpg.set_primary_window("Main", True)
        dpg.set_viewport_max_width(1400) #500
        dpg.set_viewport_max_height(700) #350
        dpg.set_viewport_pos([(screenwidth/2-200), (screenheight/2-150)])
        #dpg.set_viewport_resizable(False)
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

                            with dpg.table_row():dpg.add_combo(tag="WEAPONS", items=WEAPONS, default_value=DEF_WEAPON,
                                                    callback=currentWeaponCallback,
                                                    width=100)
                                
                            #Float Input
                            with dpg.table_row():dpg.add_text("Float")
                            with dpg.table_row():
                                dpg.add_input_float(tag="Float_value", min_value=0.000001, max_value=0.999999,
                                                    step=0.1, min_clamped=True, max_clamped=True,
                                                    format='%.6f', default_value=DEF_FLOAT,
                                                    callback=saveConfig,
                                                    width=220)
                                
                            #Seed Input
                            with dpg.table_row():dpg.add_text("Seed")
                            with dpg.table_row():dpg.add_input_int(tag="seed_value", max_value=1000, min_value=0,
                                                    max_clamped=True, min_clamped=True, default_value=DEF_SEED,
                                                    callback=saveConfig,
                                                    width=220)
                                
                            
                            #Stattrak Input
                            with dpg.table_row():dpg.add_checkbox(tag="stattrak_bool", label="StatTrak", default_value=DEF_STATTRAK,
                                                    callback=saveConfig)
                            with dpg.table_row():dpg.add_input_int(tag="stattrak_value", max_value=999999, min_value=1,
                                                    max_clamped=True, min_clamped=True, default_value=DEF_STATTRAK_VALUE,
                                                    callback=saveConfig,
                                                    width=220)
                            
                            with dpg.table_row():dpg.add_spacer(height=32)
                            with dpg.table_row():dpg.add_text(f"Current Config: {cur_configfile}")
                            with dpg.table_row():dpg.add_button(label="Force Update", width=220, callback=forceUpdate)
                            with dpg.table_row():dpg.add_button(label="Change Config", width=220)
                                
                        
                        with dpg.table(header_row=False):
                            dpg.add_table_column()
                            
                            with dpg.table_row():dpg.add_text("Paintkits")
                            with dpg.table_row():dpg.add_input_text(tag="paintkit_seach", callback=paintkit_input_callback, width=230)
                            with dpg.table_row():dpg.add_listbox(tag="paintkit_value", items=skin_names, default_value=DEF_PAINT,
                                                    callback=saveConfig,
                                                    num_items=12, width=230)
                
            with dpg.tab(label="Settings"):
                with dpg.table(header_row=False):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    with dpg.table_row():
                        
                        with dpg.table(header_row=False):
                            dpg.add_table_column()

                            with dpg.table_row():dpg.add_text("Menu")
                            with dpg.table_row():dpg.add_separator()

    with dpg.theme() as global_theme:

        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 3, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 16, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 3, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 3, category=dpg.mvThemeCat_Core)

    dpg.bind_theme(global_theme)

    dpg.show_style_editor()

    dpg.show_viewport()
    while dpg.is_dearpygui_running():
        sleep(0.02)
        getConfig()
        dpg.render_dearpygui_frame()
    dpg.destroy_context()

if __name__ == '__main__':
    main()
    