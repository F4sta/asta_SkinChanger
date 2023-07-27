import json

n = open("netvars.json", "r")

response = json.load(n)

m_totalHitsOnServer = int(response["DT_CSPlayer"]["m_totalHitsOnServer"])
m_iViewModelIndex = int(response["DT_BaseCombatWeapon"]["m_iViewModelIndex"])
m_nModelIndex = int(response["DT_BaseViewModel"]["m_nModelIndex"])
m_hViewModel = int(response["DT_BasePlayer"]["m_hViewModel[0]"])