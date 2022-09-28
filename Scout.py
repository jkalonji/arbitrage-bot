# On met tout ensemble

import requests, json

# ================================== Fonctions =================================

def swapToRune(inputAssetAmount, inputAssetBalance, outputAssetBalance):
    return inputAssetAmount*inputAssetBalance*outputAssetBalance/((inputAssetAmount + inputAssetBalance)**2)

def swapFromRune(inputAssetAmount, inputAssetBalance, outputAssetBalance):
    return inputAssetAmount*inputAssetBalance*outputAssetBalance/((inputAssetAmount + inputAssetBalance)**2)
    
# ===================================== Main ===================================






def getSwapResults():
    url = requests.get("https://midgard.thorchain.info/v2/pools")
    text = url.text
    data = json.loads(text)

    sethBalance    = float(data[7]['assetDepth']) 
    runeDepthseth  = float(data[7]['runeDepth'])
    ethBalance     = float(data[16]['assetDepth'])
    runeBalanceeth = float(data[16]['runeDepth'])

    firstSwapOutputNatToSynth   = swapToRune(1e8, ethBalance, runeBalanceeth)
    doubleSwapOutputNatToSynth = 1e-8*swapFromRune(firstSwapOutputNatToSynth , runeDepthseth, sethBalance)
    doubleSwapOutputNatToSynth

    firstSwapOutputSynthToNat   = swapToRune(1e8,sethBalance , runeDepthseth)
    doubleSwapOutputSynthToNat = 1e-8*swapFromRune(firstSwapOutputSynthToNat ,runeBalanceeth , ethBalance)
    if doubleSwapOutputNatToSynth>1 or doubleSwapOutputSynthToNat >1:
        print('Opportunité trouvée !')
        
    return{"Nat to synth":doubleSwapOutputNatToSynth, "Synth to nat ":doubleSwapOutputSynthToNat}  # Dict contenant les résultats

	
print(getSwapResults())
