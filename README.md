# FlexpoolInfo
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
## A custom component for [HomeAssistant](https://github.com/home-assistant/core) 

Provides data from [Flexpool.io](https://flexpool.io/) on a specified miner.

If this has been of use, please consider funding my caffeine habit:

<a href="https://www.buymeacoffee.com/tomprior" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png"></a>

# Goals

* Create sensor items for Ethermine items:
  * Current statistics
  
      ✔ Unpaid balance
  
      ✔ Reported hash rate
  
      ✔ Average hash rate
  
      ✔ Current hash rate
  
      ✔ Valid shares
  
      ✔ Invalid shares
  
      ✔ Stale shares
  
      ✔ Active workers
      
      ✔ Balance
      
      ❌ Balance in local currency
     
  * Payouts
  
      ❌ Paid on
  
      ❌ Amount
  
      ❌ Transaction hash
      
      ❌ Value in local currency

## Things you should know

* This custom component is a work-in-progress item.
* Chia items are untested until a tester gets in contact with me to assist.
* There are limits on how many requests can be made to Flexpool's API and therefore the data retrieved by FlexpoolInfo will be updated periodically and may be out of date by the time you look at it.
* Please do not use FlexpoolInfo in isolation to make decisions about your cryptocurrency holdings.
* FlexpoolInfo only reads the statistics of the provided miner.

## Installation

Copy the files in the /custom_components/flexpoolinfo/ folder to: [homeassistant]/config/custom_components/flexpoolinfo/

## Configuration

To use FlexpoolInfo, please add the following items to your HomeAssistant ```configuration.yaml```
````
sensor:
  - platform: ethermineinfo
    miner_address: (required) the address of your Ethermine miner
    currency_name: (required) the currency you would like your unpaid balance to be converted to (not currently implemented)
    token: (required) the token you are mining (eth or xch)
    name_override: (optional) name to identify your wallet instead of your miner address.
    
````

Please note that the Flexpool API accepts the address in one format only; 42 characters beginning with 0x

The 42 character address *must* be encapsulated in quote marks. Failure to do so will just return "unknown" in HomeAssistant.

Examples:

```
sensor:
  - platform: flexpoolinfo
    miner_address: "0x1234567890123456789012345678901234567890"
    currency_name: USD
    token: eth
```

```
sensor:
  - platform: ethermineinfo
    miner_address: "0x1234567890123456789012345678901234567890"
    currency_name: USD
    name_override: "wallet name"
    token: xch
```

Multiple addresses can be configured.

## Templates

You can create a template sensor for any of the attributes returned by FlexpoolInfo. For example:

Stale shares:
```{{ states.sensor.flexpoolinfo_miner_address.attributes['stale_shares'] }}```

Current hashrate:
```{{ states.sensor.flexpoolinfo_miner_address.attributes['current_hashrate'] }}```

Unpaid amount:
```{{ states.sensor.flexpoolinfo_miner_address.attributes['unpaid_balance'] }}```

Pull requests and constructive criticism are always welcome.

## Credits

[@heyajohnny's](https://github.com/heyajohnny) [CryptoInfo](https://github.com/heyajohnny/cryptoinfo) from which this component was born.

[W3Schools](https://www.w3schools.com/python/default.asp) for being an invaluable learning resource.
