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

# On ne  swap qu'entre ETH et ETH binance, car c'est la paire ETH qui rassemnle le plus de volume
    sethBalance    = float(data[7]['assetDepth']) 
    runeDepthseth  = float(data[7]['runeDepth'])
    ethBalance     = float(data[16]['assetDepth'])
    runeBalanceeth = float(data[16]['runeDepth'])
    inputAmount = 10 # Vérifier l'unité de inputAmount

    firstSwapOutputNatToSynth   = swapToRune(inputAmount*1e8, ethBalance, runeBalanceeth)
    doubleSwapOutputNatToSynth = 1e-8*swapFromRune(firstSwapOutputNatToSynth , runeDepthseth, sethBalance)
    doubleSwapOutputNatToSynth

    firstSwapOutputSynthToNat   = swapToRune(inputAmount*1e8,sethBalance , runeDepthseth)
    doubleSwapOutputSynthToNat = 1e-8*swapFromRune(firstSwapOutputSynthToNat ,runeBalanceeth , ethBalance)
    if doubleSwapOutputNatToSynth>inputAmount or doubleSwapOutputSynthToNat >inputAmount:
        print('Opportunité trouvée !')
        
    return{"Nat to synth":doubleSwapOutputNatToSynth, "Synth to nat ":doubleSwapOutputSynthToNat}  # Dict contenant les résultats

	
	
while(True):
    try:
        print(getSwapResults())
    except:
        pass
