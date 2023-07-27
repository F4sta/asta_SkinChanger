import dearpygui.dearpygui as dpg
import json
import ctypes
user32 = ctypes.windll.user32
screenwidth, screenheight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
from configparser import ConfigParser
c = ConfigParser()
c.read("Config/Custom1.ini")
with open("skin_dict.json", "r", encoding="utf-8") as file:Skin_dict = dict(json.load(file))

skin_names = list(Skin_dict.keys())
rifles = "ak47","m4a4","m4a1s","galiar","famas","awp","ssg08"
pistols = "usp","glock","deagle","p250","fiveseven","tec9","revolver"

def_rifle_weapon = rifles[0]
def_rifle_paintkit = skin_names[0]
def_rifle_float = 0.000001
def_rifle_seed = 0
def_rifle_stattrak = False
def_rifle_stattrak_value = 1

cur_rifle_weapon = def_rifle_weapon
cur_rifle_paintkit = def_rifle_paintkit
cur_rifle_float = def_rifle_float
cur_rifle_seed = def_rifle_seed
cur_rifle_stattrak = def_rifle_stattrak
cur_rifle_stattrak_value = def_rifle_stattrak_value

def getIdByPaintkit(paintkit):
    return Skin_dict[paintkit]

def save_config(configType, weapon, value):
    c[configType][weapon] = value
    with open("Config/Custom1.ini", "w", encoding="utf-8") as file:
        c.write(file)

def currentWeaponCallback(Sender):
    global cur_rifle_weapon
    weapon = str(dpg.get_value(Sender))
    cur_rifle_weapon = weapon

def paintkit_input_callback(Sender):
    configType = "Skins"
    paintkit_input = str(dpg.get_value(Sender))
    for i in skin_names:
        if paintkit_input.lower() == str(i).lower():
            dpg.set_value("paintkit_combo", i)
            save_config(configType, "ak47", getIdByPaintkit(i))
    
def config_callbacks(sender, Type):
    configType = f"{Type}"
    var = dpg.get_value(sender)
    if configType == "Float":
        var = "{:.6f}".format(var)
        if var == "1e-06":
            var = "0.000001"
    elif configType == "Skins":
        var = getIdByPaintkit(var)
    save_config(configType, cur_rifle_weapon, str(var))
    
def main():
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()

    with dpg.window(label="Main", tag="Main"):
        
        #Setting the main window
        dpg.set_primary_window("Main", True)
        dpg.set_viewport_max_width(400)
        dpg.set_viewport_max_height(300)
        dpg.set_viewport_pos([(screenwidth/2-200), (screenheight/2-150)])
        dpg.set_viewport_resizable(False)
        dpg.set_viewport_title("asta's Skinschanger")
        
        
        
        with dpg.tab_bar(tag="MainTab"):
            with dpg.tab(label="Rifles"):
                with dpg.table(header_row=False):
                    
                    dpg.add_table_column()
                    dpg.add_table_column()

                    with dpg.table_row():
                        dpg.add_combo(tag="rifle-weapons", items=rifles, default_value=def_rifle_weapon,
                                    callback=currentWeaponCallback)
                        
                    with dpg.table_row():
                        dpg.add_text("Paintkits")
                        dpg.add_input_text(callback=paintkit_input_callback)
                        
                    with dpg.table_row():
                        dpg.add_text()
                        dpg.add_combo(tag="paintkit_combo" ,items=skin_names, default_value=def_rifle_paintkit,
                                            callback=lambda : config_callbacks(sender = "paintkit_combo", Type="Skins"))
                        
                    with dpg.table_row():
                        dpg.add_text("Float")
                        dpg.add_input_float(tag="Float_input", min_value=0.000001, max_value=0.999999,
                                            step=0.1, min_clamped=True, max_clamped=True,
                                            format='%.6f', default_value=def_rifle_float,
                                            callback=lambda : config_callbacks(sender = "Float_input", Type="Float"))
                    with dpg.table_row():
                        dpg.add_text("Seed")
                        dpg.add_input_int(tag="seed_value", max_value=1000, min_value=0,
                                            max_clamped=True, min_clamped=True, default_value=def_rifle_seed,
                                            callback=lambda : config_callbacks(sender = "seed_value", Type="Seed"))
                        
                    with dpg.table_row():
                        dpg.add_text("StatTrak")
                        dpg.add_checkbox(tag="stattrak_bool", default_value=def_rifle_stattrak,
                                            callback=lambda : config_callbacks(sender = "stattrak_bool", Type="Stattrak"))
                        
                    with dpg.table_row():
                        dpg.add_text()
                        dpg.add_input_int(tag="stattrak_value", max_value=999999, min_value=1,
                                            max_clamped=True, min_clamped=True, default_value=def_rifle_stattrak_value,
                                            callback=lambda : config_callbacks(sender = "stattrak_value", Type="StattrakValue"))

        
            with dpg.tab(label="Pistols"):
                pass
            
            with dpg.tab(label="Settings"):
                pass
        

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    main()
    