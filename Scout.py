# On met tout ensemble

import requests, json

# ================================== Fonctions =================================

def swapToRune(inputAssetAmount, inputAssetBalance, outputAssetBalance):
    return inputAssetAmount*inputAssetBalance*outputAssetBalance/((inputAssetAmount + inputAssetBalance)**2)

def swapFromRune(inputAssetAmount, inputAssetBalance, outputAssetBalance):
    return inputAssetAmount*inputAssetBalance*outputAssetBalance/((inputAssetAmount + inputAssetBalance)**2)
    
# ===================================== Main ===================================

url = requests.get("https://midgard.thorchain.info/v2/pools")
text = url.text
data = json.loads(text)

sethBalance    = float(data[6]['assetDepth']) 
runeDepthseth  = float(data[6]['runeDepth'])
ethBalance     = float(data[15]['assetDepth'])
runeBalanceeth = float(data[15]['runeDepth'])

firstSwapOutputNatToSynth   = swapToRune(1e8, ethBalance, runeBalanceeth)
doubleSwapOutputNatToSynth = 1e-8*swapFromRune(firstSwapOutputNatToSynth , runeDepthseth, sethBalance)
doubleSwapOutputNatToSynth

firstSwapOutputSynthToNat   = swapToRune(1e8,sethBalance , runeDepthseth)
doubleSwapOutputSynthToNat = 1e-8*swapFromRune(firstSwapOutputSynthToNat ,runeBalanceeth , ethBalance)

print('doubleSwapOutputNatToSynth: ', doubleSwapOutputNatToSynth)
print('doubleSwapOutputSynthToNat: ', doubleSwapOutputSynthToNat)
