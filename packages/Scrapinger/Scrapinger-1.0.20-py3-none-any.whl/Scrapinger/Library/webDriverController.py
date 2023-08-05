import LibHanger.Library.uwLogger as Logger
from Scrapinger.Library.baseWebBrowserController import baseWebBrowserController
from Scrapinger.Library.browserContainer import browserContainer
from Scrapinger.Library.scrapingConfig import scrapingConfig
from Scrapinger.Library.scrapingerException import scrapingerException

class webDriverController(baseWebBrowserController):
    
    """
    WebDriverコントローラークラス
    
    Notes
    -----
        取り扱うWebDriverをブラウザータイプごとに取得する
    """ 

    def __init__(self, _config:scrapingConfig, _browserContainer:browserContainer):
        
        """
        コンストラクタ
        
        Parameters
        ----------
        _config : scrapingConfig
            共通設定クラス
        _browserContainer : browserContainer
            ブラウザコンテナクラス

        """ 
        
        # 共通設定取得
        self.config = _config
        
        # ブラウザーコンテナインスタンス設定
        self.browserContainerInstance = _browserContainer
        
        # ブラウザーコントロールインスタンス初期化
        self.browserCtl = None

    @Logger.loggerDecorator('Setting Scrape')    
    def settingScrape(self):
        
        """
        スクレイピング準備
        """
        
        if self.config.ScrapingType == scrapingConfig.settingValueStruct.ScrapingType.beutifulSoup.value:
            self.getBeautifulSoupInstance()
        elif self.config.ScrapingType == scrapingConfig.settingValueStruct.ScrapingType.selenium.value:
            self.getWebDriverInstance()
    
    @Logger.loggerDecorator('Get BeautifulSoupInstance')    
    def getBeautifulSoupInstance(self):
        
        """
        BeautifulSoupインスタンスを取得する
        """ 
        
        if self.config.ScrapingType == scrapingConfig.settingValueStruct.ScrapingType.beutifulSoup.value:
            self.browserCtl = self.browserContainerInstance.beautifulSoup(self.config)
        else:
            # 例外とする
            raise scrapingerException.scrapingTypeErrorException
    
    @Logger.loggerDecorator('Get WebDriverInstance')
    def getWebDriverInstance(self):
        
        """
        WebDriverインスタンスを取得する
        """ 

        # ブラウザータイプごとに生成するインスタンスを切り替える
        browserName = 'unknown'
        if self.config.BrowserType == scrapingConfig.settingValueStruct.BrowserType.chrome.value:
            self.browserCtl = self.browserContainerInstance.chrome(self.config)
            browserName = scrapingConfig.settingValueStruct.BrowserType.chrome.name
        elif self.config.BrowserType == scrapingConfig.settingValueStruct.BrowserType.firefox.value:
            self.browserCtl = self.browserContainerInstance.firefox(self.config)
            browserName = scrapingConfig.settingValueStruct.BrowserType.firefox.name
        else:
            # 例外とする
            raise scrapingerException.scrapingTypeErrorException
        
        # 取得したWebDriverをログ出力
        Logger.logging.info('BrowserType:' + str(self.config.BrowserType))
        Logger.logging.info('SelectedBrowser:' + browserName)

        # 取得したWebDriverインスタンスを返す
        return self.browserCtl.getWebDriver()

