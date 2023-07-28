''' Updating offsets '''

import offsets_dumper
offsets_dumper.update_offsets()
try:from offsets import *
except:offsets_dumper.update_offsets();from offsets import *

''' Importing Libraries '''

from time import sleep
from pymem import *

def GetWeaponPaint(itemDefiniton : int):
    match itemDefiniton:
        
        case 7:  return 1035   # ak
        case 16:  return 0   # m4a4
        case 60:  return 0   # m4a1-s
        case 13:  return 0   # galiar
        case 10:  return 0   # famas
        case 9:  return 51   # awp
        case 40:  return 0   # ssg-08
        
        case 61:  return 653   # usp
        case 4:  return 38   # glock
        case 1:  return 711   # deagle
        case 36:  return 0   # p250
        case 3:  return 0   # five-seven
        case 30:  return 0   # tec-9
        case 64:  return 0   # revolver
        
        case _ : return 0   # Default Acction

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
        except:
            continue
    
    Seed = 0
    FLoat = 0.0001
    Statrak = True
    Statrak_value = 69
    
    #skinchanger loop
    print("SkinChanger Started...")
    run = True
    while run:
        sleep(0.002)
        
        localPlayer = pm.read_uint( client + dwLocalPlayer )
        
        #local player weapon iteration
        for i in range( 0, 8 ):
            weapons =  pm.read_uint( localPlayer + m_hMyWeapons + (i - 1) * 0x4 ) & 0xFFF
            weapon_address = pm.read_uint( client + dwEntityList + (weapons - 1) * 0x10 )

            # checking if weaopon is valid
            if not weapon_address:
                continue
            
            paint = GetWeaponPaint(pm.read_short( weapon_address + m_iItemDefinitionIndex ))
            if paint:
                shouldUpdate = pm.read_int( weapon_address + m_nFallbackPaintKit ) != paint
                
                #force weapon to use fallback values
                pm.write_int( weapon_address + m_iItemIDHigh, -1 )
                
                #float
                pm.write_int( weapon_address + m_nFallbackPaintKit, paint)
                pm.write_float( weapon_address + m_flFallbackWear, FLoat )
                
                #seed
                pm.write_int( weapon_address + m_nFallbackSeed, Seed )
                
                #statrak
                if Statrak:
                    weapon_owner = pm.read_int( weapon_address + m_OriginalOwnerXuidLow )
                    pm.write_int( weapon_address + m_iAccountID, weapon_owner )
                    pm.write_int( weapon_address + m_nFallbackStatTrak, Statrak_value )
                
                if shouldUpdate:
                    pm.write_int(pm.read_uint( engine + dwClientState ) + 0x174, -1)
            

if __name__ == '__main__':
    main()