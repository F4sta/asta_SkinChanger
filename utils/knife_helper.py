
from enum import Enum
class ItemDefinitionIndex(Enum):
    #Knifes
	WEAPON_KNIFE_CT = 42
	WEAPON_KNIFE_T = 59
	WEAPON_KNIFE_BAYONET = 500
	WEAPON_KNIFE_CLASSIC = 503
	WEAPON_KNIFE_FLIP = 505
	WEAPON_KNIFE_GUT = 506
	WEAPON_KNIFE_KARAMBIT = 507
	WEAPON_KNIFE_M9_BAYONET = 508
	WEAPON_KNIFE_HUNTSMAN = 509
	WEAPON_KNIFE_FALCHION = 512
	WEAPON_KNIFE_BOWIE = 514
	WEAPON_KNIFE_BUTTERFLY = 515
	WEAPON_KNIFE_SHADOWDAGGERS = 516
	WEAPON_KNIFE_PARACORD = 517
	WEAPON_KNIFE_CANIS = 518
	WEAPON_KNIFE_URSUS = 519
	WEAPON_KNIFE_NAVAJA = 520
	WEAPON_KNIFE_SURIVIAL = 521
	WEAPON_KNIFE_STILETTO = 522
	WEAPON_KNIFE_TALON = 523
	WEAPON_KNIFE_SKELETON = 525

	''' #Gloves
	GLOVE_STUDDED_BLOODHOUND = 5027
	GLOVE_T_SIDE = 5028
	GLOVE_CT_SIDE = 5029
	GLOVE_SPORTY = 5030
	GLOVE_SLICK = 5031
	GLOVE_LEATHER_WRAP = 5032
	GLOVE_MOTORCYCLE = 5033
	GLOVE_SPECIALIST = 5034
	GLOVE_HYDRA = 5035 '''

knifeIndexes = [i.value for i in ItemDefinitionIndex]