import LibHanger.Library.uwLogger as Logger
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.firefox.options import Options as firefoxOptions
from LibHanger.Library.uwGlobals import *
from Scrapinger.Library.baseWebBrowserController import baseWebBrowserController
from Scrapinger.Library.scrapingConfig import scrapingConfig

class browserContainer:
    
    """
    ブラウザコンテナクラス
    """

    class beautifulSoup(baseWebBrowserController):
    
        """
        beautifulSoup用コンテナ
        """
    
        def __init__(self, _config: scrapingConfig):
            
            """
            コンストラクタ
            
            Parameters 
            ----------
            _config : scrapingConfig
                共通設定クラス

            """
            
            # 基底側コンストラクタ呼び出し
            super().__init__(_config)
    
    class chrome(baseWebBrowserController):
        
        """
        GoogleCheromブラウザコンテナ
        """
        
        def __init__(self, _config:scrapingConfig):
            
            """
            コンストラクタ
            
            Parameters 
            ----------
            _config : scrapingConfig
                共通設定クラス

            """
            
            # 基底側コンストラクタ呼び出し
            super().__init__(_config)
            
        def getWebDriver(self):
            
            """ 
            Webドライバーを取得する
            
            Parameters
            ----------
            None
                
            """
            
            # オプションクラスインスタンス
            options = chromeOptions()
            # ヘッドレスモード設定
            options.add_argument('--headless')
            # WebDriverパスを取得
            webDriverPath = self.getWebDriverPath(self.config.chrome)
            # WebDriverを返す
            if self.config.chrome.WebDriverLogPath == '':
                self.wDriver = webdriver.Chrome(executable_path=webDriverPath, options=options)
            else:
                self.wDriver = webdriver.Chrome(executable_path=webDriverPath, log_path=self.config.chrome.WebDriverLogPath, options=options)
            return self.wDriver 
        
    class firefox(baseWebBrowserController):
        
        """
        FireFoxブラウザコンテナ
        """
        
        def __init__(self, _config:scrapingConfig):
            
            """
            コンストラクタ
            
            Parameters 
            ----------
            _config : scrapingConfig
                共通設定クラス

            """
            
            # 基底側コンストラクタ呼び出し
            super().__init__(_config)
            
        def getWebDriver(self):
            
            """ 
            Webドライバーを取得する
            
            Parameters
            ----------
            None
                
            """
                        
            # オプションクラスインスタンス
            options = firefoxOptions()
            # ヘッドレスモード設定
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')            
            # WebDriverパスを取得
            webDriverPath = self.getWebDriverPath(self.config.firefox)
            # WebDriverを返す
            Logger.logging.info('get webdriver - start')
            Logger.logging.info(self.config.firefox.WebDriverLogPath)
            try:
                if self.config.firefox.WebDriverLogPath == '':
                    self.wDriver = webdriver.Firefox(executable_path=webDriverPath, options=options)
                else:
                    self.wDriver = webdriver.Firefox(executable_path=webDriverPath, log_path=self.config.firefox.WebDriverLogPath, options=options)            
                Logger.logging.info('get webdriver - end')
            except WebDriverException as e:
                Logger.logging.info("Selenium Exception: {0} Message: {1}".format("WebDriverException", str(e)))
            except TimeoutException as e:
                Logger.logging.info("Selenium Exception: {0} Message: {1}".format("TimeoutException", str(e)))                
            return self.wDriver 
