
import { assetToBase, baseToAsset, assetAmount, AssetRuneNative, baseAmount } from "@xchainjs/xchain-util"
import { Client } from '@xchainjs/xchain-thorchain';
import { Network } from '@xchainjs/xchain-client'
import {XMLHttpRequest} from 'xmlhttprequest'


var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};


// initialisation du client
async function test() {
	const mainnet_address_path0 = 'thor1twqpf8dkdn5p6w9grqrxl0u9agzx6vxjx958fy'

	const phrase = 'alert kind salmon merit possible company ritual armor vivid order security arena'
	const chainIds = {
		[Network.Mainnet]: "thorchain-mainnet-v1"
	}

	const DEPOSIT_GAS_LIMIT_VALUE = '600000000'
	let thorClient = new Client({ phrase, network: Network.Mainnet, chainIds })
	//console.log('thorClient: '+Object.entries(thorClient))

	let cosmosClient = thorClient.getCosmosClient()
	//let balance = await thorClient.getBalance('thor1twqpf8dkdn5p6w9grqrxl0u9agzx6vxjx958fy', AssetRuneNative, cosmosClient)
	//console.log('cosmosClient :'+Object.keys(cosmosClient))


	let address = thorClient.getAddress(0)
	console.log('address ->'+address+'<-')

	  
	  
	let walletIndex = 0
	let asset = AssetRuneNative  // Pour l'instant on n'envoie que de la RUNE
	var amount = baseAmount(0.1*1e8) // ici on envoi 0.1 rune (multiplier par 1e8)
	var memo = 'swap:BNB/BUSD-BD1:thor1twqpf8dkdn5p6w9grqrxl0u9agzx6vxjx958fy'
	console.log('amount dans le code : '+ amount)

/*
	await thorClient.deposit({
	asset : asset,
    amount: amount,
	memo:memo });*/
}

test()

getJSON('http://127.0.0.1:5001',
function(err, data) {
  if (err !== null) {
    alert('Something went wrong: ' + err);
  } else {
    alert('Your query count: ' + data.query.count);
    console.log(data.query.count)
  }
});


