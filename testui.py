from dearpygui.dearpygui import *
import json

with open("skin_dict.json", "r", encoding="utf-8") as file:Skin_dict = dict(json.load(file))

skin_names = list(Skin_dict.keys())
temp_skinnames = skin_names

def input_text_callback(Sender):
    paintkit_input = str(get_value(Sender))
    if not paintkit_input == "":
        temp_skinnames = [] 
        for i in skin_names:
            if paintkit_input.lower() in str(i).lower():
                temp_skinnames.append(i)
            if i == skin_names[-1]:
                configure_item("paintkit_listbox", items=temp_skinnames)
        print(len(skin_names),len(temp_skinnames))
    else:temp_skinnames = skin_names;configure_item("paintkit_listbox", items=temp_skinnames)

create_context()
create_viewport()
setup_dearpygui()

with window(label="Main", tag="Main"):
    
    #Setting the main window
    set_primary_window("Main", True)
    set_viewport_max_width(400)
    set_viewport_max_height(300)
    set_viewport_resizable(False)
    set_viewport_title("asta's Skinschanger")
    
    
    
    with tab_bar(tag="MainTab"):
        with tab(label="Rifles"):
            add_input_text(callback=input_text_callback)
            add_listbox(tag="paintkit_listbox", items=temp_skinnames, num_items=10)
            

show_viewport()
start_dearpygui()
destroy_context()
