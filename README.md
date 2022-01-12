# FlexpoolInfo
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
## A custom component for [HomeAssistant](https://github.com/home-assistant/core) 

Provides data from [Flexpool.io](https://flexpool.io/) on a specified miner.

If this has been of use, please consider funding my caffeine habit:

<a href="https://www.buymeacoffee.com/tomprior" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png"></a>

# Goals

* Create sensor items for Flexpool API items:
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
      
      ✔ Balance in local currency
     
  * Payouts
  
      ✔ Paid on
  
      ✔ Amount
  
      ✔ Transaction hash
      
      ✔ Value in local currency

## Things you should know about FlexpoolInfo
* The Flexpool API is subject to change - there may be occaisions where a code change is required before the component will work again.
* There are limits on how many requests can be made to Flexpool's API and therefore the data retrieved by FlexpoolInfo will be updated periodically and may be out of date by the time you look at it.
* Please do not use FlexpoolInfo in isolation to make decisions about your cryptocurrency holdings.
* FlexpoolInfo only reads the statistics of the provided miner.

## Pre-requisite knowledge

Before downloading and configuring FlexpoolInfo, please ensure you are familiar with the following items:

* HomeAssistant's configuration file [LINK](https://www.home-assistant.io/docs/configuration/)
* YAML syntax [LINK](https://www.home-assistant.io/docs/configuration/yaml/)
* Installation of custom components via:
  * HACS [LINK](https://hacs.xyz/docs/setup/prerequisites)
  * Manual custom component installation
* Adding template sensors to your configuration [LINK](https://www.home-assistant.io/integrations/template/)

## Installation

Copy the files in the /custom_components/FlexpoolInfo/ folder to: [homeassistant]/config/custom_components/FlexpoolInfo/

HACS users, you know what to do!
In case you don't:

1. Open HACS from your HomeAssistant sidebar
2. Press the "Explore & Add Repositories"
3. Enter "FlexpoolInfo" into the search box
4. Press "FlexoolInfo"
5. Press "Install this repository in HACS"
6. Don't forget to complete the configuration before restart HomeAssistant!

## Configuration

To use FlexpoolInfo, please add the following items to your HomeAssistant ```configuration.yaml```
````
sensor:
  - platform: FlexpoolInfo
    miner_address: (required) the address of your Ethermine miner
    currency_name: (required) the currency you would like your unpaid balance to be converted to
    token: (required) XCH or ETH
    name_override: (optional) name to identify your wallet instead of your miner address.
````

Please note that the Ethermine API accepts the address in two formats:

- ETH: 42 characters beginning with 0x
- XCH: 62 characters beggining with xch1

The address must be encapsulated in quotation marks as follows:

Examples:

```
sensor:
  - platform: flexpoolinfo
    miner_address: "0x1234567890123456789012345678901234567890"
    currency_name: USD
    token: ETH
```

```
sensor:
  - platform: flexpoolinfo
    miner_address: "xch12345678901234567890123456789012345678901234567890123456789"
    currency_name: USD
    token: XCH
```

Multiple addresses can be configured.

## Templates

You can create a template sensor for any of the attributes returned by FlexpoolInfo. For example:

Stale shares:
```{{ states.sensor.FlexpoolInfo_miner_address.attributes['stale_shares'] }}```

Current hashrate:
```{{ states.sensor.FlexpoolInfo_miner_address.attributes['current_hashrate'] }}```

Unpaid amount:
```{{ states.sensor.FlexpoolInfo_miner_address.attributes['unpaid_balance'] }}```

## How does it look?
![Untitled](https://user-images.githubusercontent.com/34111848/143680739-d6869fb5-ea10-4f9e-b9e2-fa5b2e300f96.png)

Disclaimer: I do not mine cryptocurrency. This screenshot is from a publicly accessible address on Flexpool. Some information has been redacted in the image above to protect the privacy of the individual.

Some rather pretty graphs are possible with the [mini-graph-card](https://github.com/kalkih/mini-graph-card):

![image](https://user-images.githubusercontent.com/34111848/143507616-a8bac318-5696-4a8a-bffe-7f4d14c8f5e5.png)

## Discussion

[Talk about FlexpoolInfo here](https://community.home-assistant.io/t/my-first-custom-component-FlexpoolInfo/302734)

[Post issues with FlexpoolInfo here](https://github.com/ThomasPrior/FlexpoolInfo/issues)

Issues should be posted with logs and relevant, redacted excerpts from your configuration.yaml file to ensure that help can be given most effectively.

Pull requests and constructive criticism are always welcome.

## Credits

[@heyajohnny's](https://github.com/heyajohnny) [CryptoInfo](https://github.com/heyajohnny/cryptoinfo) from which this component was born.

[W3Schools](https://www.w3schools.com/python/default.asp) for being an invaluable learning resource.
