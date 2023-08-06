# **igeSdk**
igeSdk is a compilation of all necessary third party SDKs in order to make your game ready to be published, which contains Analytics, Advertisement, InAppPurchase and CrossPromotion features.

The current implementation status is as below:
- [x] Analytics : Ready (v0.0.1)
- [x] Advertisement : Ready (v0.0.2)
- [x] InAppPurchase : Ready (v0.0.3)
- [x] CrossPromotion : Ready (v0.0.4)

*The SDK supports **Android** and **iOS** platforms. On unsupported platforms (Windows, Linux, MacOS, ...), it the code still running with dummy functionalities.*

## **Configuration and Initialization**
To config the SDK, you need to create `igeSdk.config` which is a json file contains settings for different modules.

Configuration for Advertisement, InAppPurchase and CrossPromotion is WIP.

To initialize the SDK, just `import igeSdk` and call `init()` method in your main logic code, like below:
```py
import igeSdk

class GameManager(Script):

    def onStart(self):
        igeSdk.init()
        # Other initialization stuffs
```

The code above will inialize all the enabled modules which are configured in the configuration file.

*Notice, the SDK only initialize modules which have been configured. So, to disable unwanted modules, just remove their settings out of the configuration file.*

## **Analytic**

The Analytics module is used in order to send informations to the different analytics platforms. We are currently using Facebook, GameAnalytics and AppsFlyer.

To configure Analytics features, put those settings into `igeSdk.config`:
```json
{
  "android" : {
    "FacebookAppId": "",
    "FacebookClientToken": "",
    "AppsFlyerApiKey": "",
    "AppsFlyerAppId": "",
    "GameAnalyticsGameKey": "",
    "GameAnalyticsSecretKey": "",
  },
  "ios" : {
    "FacebookAppId": "",
    "FacebookClientToken": "",
    "AppsFlyerApiKey": "",
    "AppsFlyerAppId": "",
    "GameAnalyticsGameKey": "",
    "GameAnalyticsSecretKey": "",
  }
}
```

Trackers for Advertisement, InAppPurchase and CrossPromotion modules are sent automatically by the SDK. Game developers should only focus on Progression and Design events to boost their games' performance and revenues, using API below:
```py
import igeSdk
from igeSdk import Analytics

# Level started event: send when player start new level
Analytics.levelStarted(levelName: str)

# Level passed event: send when player successfully passed the level
Analytics.levelPassed(levelName: str, score: int)

# Level failed event: send when player failed the level
Analytics.levelFailed(levelName: str, score: int)

# Custom event: used to track other stuffs like game design events, game states, ...
Analytics.customEvent(eventName: str, eventValue_optional: float)

```

## **Advertisement**
Advertisement module handles all ad-related operations for you, by implementing AppLovin MAX solution. This module provides methods for Banner, Interstitial and Rewarded Video ads, accessible with `igeSdk.Advertisement` module.

### **Configuration**
To configure Advertisement features, put those settings into `igeSdk.config`:
```json
{
  "android" : {
    "Mediation": "MAX",
    "MediationAppId" : "",
    "AdMobAppId" : "",
    "BannerId" : "",
    "InterstitialId" : "",
    "RewardedVideoId" : ""
  },
  "ios" : {
    "Mediation": "MAX",
    "MediationAppId" : "",
    "AdMobAppId" : "",
    "BannerId" : "",
    "InterstitialId" : "",
    "RewardedVideoId" : ""
  }
}
```

### **Showing/Hiding Banner**
To show/hide banner ads, use methods below:
```py
from igeSdk import Advertisement

Advertisement.showBanner(position: int, callback: Callable[[errCode: int, message: str], None])
Advertisement.hideBanner(callback: Callable[[errCode: int, message: str], None])
```

In which:
- `position`: [Optional] one of values below, default to `igeSdk.AdPosition_BottomCenter`.
  - `igeSdk.AdPosition_TopLeft`
  - `igeSdk.AdPosition_TopCenter`
  - `igeSdk.AdPosition_TopRight`
  - `igeSdk.AdPosition_CenterLeft`
  - `igeSdk.AdPosition_Centered`
  - `igeSdk.AdPosition_CenterRight`
  - `igeSdk.AdPosition_BottomLeft`
  - `igeSdk.AdPosition_BottomCenter`
  - `igeSdk.AdPosition_BottomRight`
- `callback`: [Optional] callback function.

### **Showing Interstitial**
To show interstitial ads, use method below:
```py
from igeSdk import Advertisement

Advertisement.showInterstitial(placement: str, callback: Callable[[errCode: int, message: str], None])
```

In which:
- `placement`: [Optional] placement id as string, default is `'default'`.
- `callback`: [Optional] callback function.

You can also check if interstitial ads is available (to display a button for example), using `Advertisement.isInterstitialAvailable()`.

### **Showing Rewarded Video**
To show rewarded video ads, use method below:
```py
from igeSdk import Advertisement

Advertisement.showRewardedVideo(placement: str, callback: Callable[[errCode: int, message: str, reward_type: str, reward_amount: float], None])
```

In which:
- `placement`: [Optional] placement id as string, default is `'default'`.
- `callback`: [Optional] callback function.

You can also check if rewarded video ads is available (to display a button for example), using `Advertisement.isRewardedVideoAvailable()`.

## **InAppPurchase**
InAppPurchase module allows you to simply integrate cross-platform In App Purchase (IAP) into your game. The module support iOS and Android billing systems.

### **Configuration**
To configure InAppPurchase module, put those settings into `igeSdk.config`:
```json
{
  "android" : {
    "IAPProductIds" : [
        "net.indigames.bundle.noads"
    ],
    "IAPPublicKey" : "YOUR APP PUBLIC KEY FROM GOOGLE PLAY CONSOLE"
  },
  "ios" : {
    "IAPProductIds" : [
        "net.indigames.bundle.noads"
    ]
  }
}
```
IAPProductIds is a list of product IDs that have been registed with Google Play Store and Apple AppStore.

To register products, please follow documents below:
- [Google Play Console](https://support.google.com/googleplay/android-developer/answer/1153481)
- [Apple AppStore Connect](https://help.apple.com/app-store-connect/#/devae49fb316)

#### **NoAds IAP**
To register NoAds IAP, you need to register a product ID which contain `noads` text, which is a non-consummable item. The logic of checking and disabling ads is automatically done by the SDK without needs of extra works from developers.

### **List Products**
To get the list of products available on store, use function below:
```py
from igeSdk import InAppPurchase

InAppPurchase.listProducts(callback: Callable[[status: int, products: List[IAPProduct]], None])
```
In which:
- callback: The callback funtion once the product list fetched, or failed in case of error.

Example:
```py
from igeSdk import InAppPurchase

class GameManager(Script):
  ....

  def listProductsCallback(self, status, products):
    if status == 0 and len(products) > 0:
      for product in products:
        print(f"{product.id} - {product.title} - {product.price} - {product.locale}")
    else:
      print("[WARN] listProductsCallback: there is no product on store, please ensure you have product ids added in igeSdk, and your app is already previewed by Apple / Google")

  def onStart(self):
    InAppPurchase.listProducts(self.listProductsCallback)
```

*Notice, you should only show `NoAds` button after fetched the product list, because if the products are not ready and if the purchase called it will do nothing which may confuse users.*

### **Purchase**
To purchase a product, use function below:
```py
from igeSdk import InAppPurchase

InAppPurchase.purchase(productId: str, callback: Callable[[status: int, products: List[IAPProduct]], None])
```
In which:
- productId: the product Id
- callback: The callback funtion once the product is purchased, or failed in case of error.

Example:
```py
from igeSdk import InAppPurchase
class BtnNoAds(Script):
  ....

  def purchaseCallback(self, status, products):
    if status == 0 and len(products) > 0:
      for product in products:
        print(f"Purchased: {product.id} - {product.title} - {product.price} - {product.locale}")
    else:
      print("[WARN] listProductsCallback: there is no product on store, please ensure you have product ids added in igeSdk, and your app is already previewed by Apple / Google")

  def onClick(self):
    InAppPurchase.purchase('', self.purchaseCallback)
```

- *The `NoAds` result is handled internally. If the transaction is a success, the banner will be hidden and all interstitial requests will be blocked*
- *Depending on the user's connection, the transaction can take a certain amount of time, we suggest you to block any playable input once a transaction is initiated and to display a loading screen showing the user that the purchase is processing.*
- *If an error occurs during the transaction, the purchaseResult callback will send you an error reason that you should display on screen.*
  - *-1: `Failed`, general issue like connection, IAP setting, ...*
  - *0: `Succeed`*
  - *1: `NotInitialized`, the purchase/restore function has been called when the IAP module is initializing*
  - *2: `IdentifierNotFound`, the productID not found on store*
  - *3: `InvalidReceipt`, receipt validation failed, which mean this maybe tampering issue with the receipt.*
  - *4: `NoRestorablePurchase`, when call restore but not made a purchase before*
  - *5: `AlreadyPurchased`, non-consummable product has already been purchased, so just need to restore or get it for free.*

### **Restore**
In case the player have purchased a Non-Consumable product (such as the IAP) and deletes the game, you need to restore their purchases.

With Google Play, the restoration is done automatic on launch. But for Apple, the restoration needs to be triggered (the user may need to re-authentify), we can't do it automatically on launch as it could be frustrating for the player to have an authentification popup at each launch.

You need to implement a Restore Purchases button somewhere in your UI to allow the restoration, this button must trigger the following function:
```py
from igeSdk import InAppPurchase

InAppPurchase.restore(callback: Callable[[status: int, products: List[IAPProduct]], None])
```
In which:
- callback: The callback funtion once the product(s) is restored, or failed in case of error.

- *The `NoAds` product restoration is handled internally.*

## **CrossPromotion**
### GDPR
The General Data Protection Regulation (GDPR) is an European data protection law that entered into force in May 2018. In order to comply with the regulation, the game need to show GDPR dialog asking for user confirmation before collecting any data from the device.

The igeSDK handled the GDPR automatically on the app's first lauch. However, it is required to add a button in game setting to access GDPR/CCPA again in order to change the setting, by calling:
```py
from igeSdk import CrossPromo
if CrossPromo.isInGdprCountry():
  CrossPromo.showGdpr()
```

### Interstitial Cross Promotion
To show interstitial we have this method:
```py
from igeSdk import CrossPromo
CrossPromo.showInterstitial()
```

### Square Cross Promotion

To show square, use method below:
```py
from igeSdk import CrossPromo
CrossPromo.showSquare(x: float, y: float, w: int, h: int)
```
In which:
- x, y: the top-left position of the square to be shown. If it is in range of 0.0 - 1.0, then it will be the percentage to the screen width and height accordingly.
- w, h: the size of the square to display.

To hide square, use method below:
```py
from igeSdk import CrossPromo
CrossPromo.hideSquare()
```
