''' Updating offsets '''
import offsets_dumper
offsets_dumper.update_offsets()
try:from offsets import *
except:offsets_dumper.update_offsets();from offsets import *

''' Getting Config '''
from configparser import ConfigParser
c = ConfigParser()
c.read("Config/Custom1.ini")
autoupdate = c["Skinchanger"]["autoupdate"]
if autoupdate == "True": autoupdate = True
else: autoupdate = False

''' Importing Libraries '''
from keyboard import is_pressed
from time import sleep
from pymem import *

def GetWeaponConfig(WeaponName):
    paint = int(c["Skins"][WeaponName])
    Float = float(c["Float"][WeaponName])
    if 0 >= Float >= 1:Float = 0.0000001
    Seed = int(c["Seed"][WeaponName])
    Stattrak = c["Stattrak"][WeaponName]
    if Stattrak == "True": Stattrak = True
    else:Stattrak = False
    Stattrak_value = int(c["StattrakValue"][WeaponName] )
    if 0 >= Stattrak_value >= 1000000:Stattrak_value = 69
        
    return paint, Float, Seed, Stattrak, Stattrak_value

def IdentifyWeapon(itemDefiniton : int):
    match itemDefiniton:
        #rifles
        case 7:  return "ak47"  # ak
        case 16:  return "m4a4"  # m4a4
        case 60:  return "m4a1s"   # m4a1-s
        case 13:  return "galiar"   # galiar
        case 10:  return "famas"   # famas
        case 9:  return "awp"  # awp
        case 40:  return "ssg08"   # ssg-08
        #pistols
        case 61:  return "usp"  # usp
        case 4:  return "glock"   # glock
        case 1:  return "deagle"   # deagle
        case 36:  return "p250"   # p250
        case 3:  return "fiveseven"   # five-seven
        case 30:  return "tec9"   # tec-9
        case 64:  return "revolver"   # revolver
        
        case _ : return None # Default Acction

def main():
    csgo_initialize  =  False
    print("Looking for csgo.exe...")
    while not csgo_initialize:
        try:
            pm = pymem.Pymem( "csgo.exe" )
            client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
            engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
            csgo_initialize  =  True
            print("CSGO initialized!")
        except:continue
    
    #skinchanger loop
    print("SkinChanger Started...")
    run = True
    while run:
        sleep(0.00002)
        
        #F6 : Force update config
        if is_pressed( "f6" ):
            c.read("Config/Custom1.ini")
            pm.write_int(pm.read_uint( engine + dwClientState ) + 0x174, -1)
        
            localPlayer = pm.read_uint( client + dwLocalPlayer )
            #local player weapon iteration
            for i in range( 0, 8 ):
                weapons =  pm.read_uint( localPlayer + m_hMyWeapons + (i - 1) * 0x4 ) & 0xFFF
                weapon_address = pm.read_uint( client + dwEntityList + (weapons - 1) * 0x10 )
                # checking if weaopon is valid
                if not weapon_address:
                    continue
                WeaponName = IdentifyWeapon(pm.read_short( weapon_address + m_iItemDefinitionIndex ))        
                if WeaponName != None:
                    #Store specific weapons config
                    paint, Float, Seed, Stattrak, Stattrak_value = GetWeaponConfig(WeaponName)
                    
                    #force weapon to use fallback values
                    pm.write_int( weapon_address + m_iItemIDHigh, -1 )
                    
                    pm.write_int( weapon_address + m_nFallbackPaintKit, paint)
                    pm.write_float( weapon_address + m_flFallbackWear, Float )
                    pm.write_int( weapon_address + m_nFallbackSeed, Seed )
                    
                    if Stattrak:
                        weapon_owner = pm.read_int( weapon_address + m_OriginalOwnerXuidLow )
                        pm.write_int( weapon_address + m_iAccountID, weapon_owner )
                        pm.write_int( weapon_address + m_nFallbackStatTrak, Stattrak_value )
                    
                    #Checks if the skinchanger needs to update
                    shouldUpdate = [ pm.read_int( weapon_address + m_nFallbackPaintKit ) != paint,
                                    pm.read_int( weapon_address + m_nFallbackSeed) != Seed ]
                    if autoupdate and any(shouldUpdate):
                        pm.write_int(pm.read_uint( engine + dwClientState ) + 0x174, -1)


if __name__ == '__main__':
    main()