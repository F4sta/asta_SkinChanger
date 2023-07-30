
import pymem
from time import sleep
from offsets import *
from utils.knife_helper import *

m_iViewModelIndex = 0x3250
m_dwModelPrecache = 0x52a4

def GetModelIndexByName(modelName: str):
    cstate = pm.read_uint(engine + dwClientState)
    nst = pm.read_uint(cstate + m_dwModelPrecache)
    nsd = pm.read_uint(nst + 0x40)
    nsdi = pm.read_uint(nsd + 0xC)
    
    for i in range(0,1024):
        nsdi_i = pm.read_uint(nsdi + 0xC + i * 0x34)
        string = pm.read_string(nsdi_i, byte = 128)
        if string == modelName:
            return int(i)
        
def GetModelIndex(itemIndex):
    match itemIndex:
        case ItemDefinitionIndex.WEAPON_KNIFE_CT.value: return GetModelIndexByName("models/weapons/v_knife_default_ct.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_T.value: return GetModelIndexByName("models/weapons/v_knife_default_t.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_BAYONET.value : return GetModelIndexByName("models/weapons/v_knife_bayonet.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_FLIP.value: return GetModelIndexByName("models/weapons/v_knife_flip.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_GUT.value: return GetModelIndexByName("models/weapons/v_knife_gut.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_KARAMBIT.value: return GetModelIndexByName("models/weapons/v_knife_karam.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_M9_BAYONET.value: return GetModelIndexByName("models/weapons/v_knife_m9_bay.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_HUNTSMAN.value: return GetModelIndexByName("models/weapons/v_knife_tactical.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_FALCHION.value: return GetModelIndexByName("models/weapons/v_knife_falchion_advanced.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_BOWIE.value: return GetModelIndexByName("models/weapons/v_knife_survival_bowie.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_BUTTERFLY.value: return GetModelIndexByName("models/weapons/v_knife_butterfly.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_SHADOWDAGGERS.value: return GetModelIndexByName("models/weapons/v_knife_push.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_URSUS.value: return GetModelIndexByName("models/weapons/v_knife_ursus.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_NAVAJA.value: return GetModelIndexByName("models/weapons/v_knife_gypsy_jackknife.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_STILETTO.value: return GetModelIndexByName("models/weapons/v_knife_stiletto.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_TALON.value: return GetModelIndexByName("models/weapons/v_knife_widowmaker.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_CLASSIC.value: return GetModelIndexByName("models/weapons/v_knife_css.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_PARACORD.value: return GetModelIndexByName("models/weapons/v_knife_cord.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_CANIS.value: return GetModelIndexByName("models/weapons/v_knife_canis.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_SURIVIAL.value: return GetModelIndexByName("models/weapons/v_knife_outdoor.mdl")
        case ItemDefinitionIndex.WEAPON_KNIFE_SKELETON.value: return GetModelIndexByName("models/weapons/v_knife_skeleton.mdl")
        case _: return 0

csgo_running = False

while not csgo_running:
    try:
        pm = pymem.Pymem("csgo.exe")
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
        engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll
        csgo_running = True
    except Exception:
        sleep(0.5)
        continue

def knifechanger():
    knifeIndex = ItemDefinitionIndex.WEAPON_KNIFE_SKELETON.value
    knifeSkin = 415
    knifeSeed = 0
    knifeFloat = 0.000000001

    itemIDHigh = -1
    entityQuality = 3
    
    modelIndex = 0
    localPlayer = 0
    
    while(True):
        sleep(0.00002)

        tempPlayer = pm.read_uint(client + dwLocalPlayer)
        if not tempPlayer: # client not connected to any server (works most of the time)
            modelIndex = 0
            continue
        elif tempPlayer != localPlayer: # local base changed (new server join/demo record)
            localPlayer = tempPlayer
            modelIndex = 0
        
        while not modelIndex:
            modelIndex = GetModelIndex(knifeIndex)

        for i in range(0,8): # loop through m_hMyWeapons slots (8 will be enough)

            # get entity of weapon in current slot
            weapon = pm.read_uint( localPlayer + m_hMyWeapons + (i - 1) * 0x4 ) & 0xFFF
            weapon_address = pm.read_uint( client + dwEntityList + (weapon - 1) * 0x10 )
            if not weapon_address:
                continue
    
            weaponIndex = pm.read_short(weapon_address + m_iItemDefinitionIndex)
            
            # for knives, set item and model related properties
            if weaponIndex == ItemDefinitionIndex.WEAPON_KNIFE_CT.value or weaponIndex == ItemDefinitionIndex.WEAPON_KNIFE_T.value or weaponIndex == knifeIndex:
                pm.write_short(weapon_address + m_iItemDefinitionIndex, knifeIndex)
                pm.write_uint(weapon_address + m_nModelIndex, modelIndex)
                pm.write_uint(weapon_address + m_iViewModelIndex, modelIndex)
                pm.write_int(weapon_address + m_iEntityQuality, entityQuality)
                    
        # get entity of weapon in our hands 
        activeWeapon = pm.read_uint(localPlayer + m_hActiveWeapon) & 0xfff
        activeWeapon_address = pm.read_uint(client + dwEntityList + (activeWeapon - 1) * 0x10)
        if not activeWeapon:
            continue
        
        # skip if current weapon is not already set to chosen knife
        weaponIndex = pm.read_short(activeWeapon_address + m_iItemDefinitionIndex)
        if weaponIndex != knifeIndex:
            continue
    
        # get viewmodel entity
        activeViewModel = pm.read_uint(localPlayer + m_hViewModel) & 0xfff
        activeViewModel = pm.read_uint(client + dwEntityList + (activeViewModel - 1) * 0x10)
        
        if not activeViewModel:
            continue
        
        pm.write_uint(activeViewModel + m_nModelIndex, modelIndex)
        
knifechanger()