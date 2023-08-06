from LibHanger.Library.uwConfig import cmnConfig
from LibHanger.Library.uwGlobals import *
from enum import Enum

class scrapingConfig(cmnConfig):

    """
    scrapinger共通設定クラス(scrapingConfig)
    """ 
    
    class settingValueStruct(cmnConfig.settingValueStruct):
        
        """
        設定値構造体
        """ 
            
        class ScrapingType(Enum):
            
            """
            スクレイピング方法
            """ 
            
            selenium = 1
            """ for selenium """ 

            beutifulSoup = 2
            """ for beutifulSoup """ 
            
        class BrowserType(Enum):
        
            """
            ブラウザータイプ
            """ 
            
            chrome = 1
            """ Google Chrome """

            firefox = 2
            """ FireFox """

            edge = 3
            """ Microsoft Edge """

        class WebDriverPath:
            
            """
            WebDriverパス
            """ 
            
            WebDriverPathWin = ''
            """ WebDriverパス for windows """

            WebDriverPathLinux = ''
            """ WebDriverパス for linux """

            WebDriverPathMac = ''
            """ WebDriverパス for mac """

            WebDriverLogPath = ''
            """ WebDriverログ出力先パス """
            
            WebDriverPath = ''
            """ WebDriverパス """
            
            def __init__(self):
                
                """ 
                コンストラクタ
                """ 

                # メンバ変数初期化
                self.WebDriverPathWin = ''
                self.WebDriverPathLinux = ''
                self.WebDriverPathMac = ''
                self.WebDriverLogPath = ''
                
    def __init__(self):
        
        """ 
        コンストラクタ
        """ 
        
        # 基底側のコンストラクタ呼び出し
        super().__init__()
        
        self.UserEgent_Mozilla = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        """ ユーザーエージェント Mozilla """

        self.UserEgent_AppleWebKit = 'AppleWebKit/537.36 (KHTML, like Gecko)'
        """ ユーザーエージェント AppleWebKit """

        self.UserEgent_Chrome = 'Chrome/94.0.4606.61 Safari/537.36'
        """ ユーザーエージェント Chrome """

        self.ScrapingType:int = self.settingValueStruct.ScrapingType.selenium.value
        """ スクレイピング方法 """

        self.BrowserType:int = self.settingValueStruct.BrowserType.chrome.value
        """ ブラウザータイプ """
        
        self.DelayTime:int = 2
        """ 1ページ読み込むごとに発生する待機時間(秒) """

        self.ItemTagName = '.ItemGrid__ItemGridCell-sc-14pfel3-1'
        """ 商品タグCSSクラス名(bs用) """
        
        self.DelayWaitElement = 'div-eagle-search-1580185158495-0'
        """ 指定されたエレメントがDOMに発生するまで待機する(WebDriver用) """
    
        self.WebDriverTimeout:int = 10
        """ Webドライバーのタイムアウト時間(秒) """
        
        self.chrome = self.settingValueStruct.WebDriverPath()
        """ Chrome-Webドライバーパス(列挙体) """
        
        self.chrome.WebDriverPathWin = ''
        """ Chrome-Webドライバーパス(Windows) """

        self.chrome.WebDriverPathLinux = ''
        """ Chrome-Webドライバーパス(Linux) """

        self.chrome.WebDriverPathMac = ''
        """ Chrome-Webドライバーパス(Mac) """

        self.chrome.WebDriverLogPath = ''
        """ Chrome-Webドライバーログ出力先パス """
        
        self.firefox = self.settingValueStruct.WebDriverPath()
        """ Firefox-Webドライバーパス(列挙体) """
        
        self.firefox.WebDriverPathWin = ''
        """ Firefox-Webドライバーパス(Windows) """

        self.firefox.WebDriverPathLinux = ''
        """ Firefox-Webドライバーパス(Linux) """

        self.firefox.WebDriverPathMac = ''
        """ Firefox-Webドライバーパス(Mac) """

        self.firefox.WebDriverLogPath = ''
        """ Firefox-Webドライバーログ出力先パス """

    def getConfigFileName(self):

        """ 
        設定ファイル名 
        """

        return 'Scrapinger.ini'
    
    def setInstanceMemberValues(self):
        
        """ 
        インスタンス変数に読み取った設定値をセットする
        """
        
        # ユーザーエージェント Mozilla
        super().setConfigValue('UserEgent_Mozilla',self.config_ini,'USER_EGENT','USEREGENT_MOZILLA',str)

        # ユーザーエージェント AppleWebKit
        super().setConfigValue('UserEgent_AppleWebKit',self.config_ini,'USER_EGENT','USEREGENT_APPLEWEBKIT',str)

        # ユーザーエージェント Chrome
        super().setConfigValue('UserEgent_Chrome',self.config_ini,'USER_EGENT','USEREGENT_CHROME',str)

        # スクレイピング方法
        super().setConfigValue('ScrapingType',self.config_ini,'SITE','SCRAPING_TYPE',int)

        # ブラウザータイプ
        super().setConfigValue('BrowserType',self.config_ini,'SITE','BROWSER_TYPE',int)

        # 待機時間
        super().setConfigValue('DelayTime',self.config_ini,'SITE','DELAY_TIME',int)

        # Webドライバータイムアウト(秒)
        super().setConfigValue('WebDriverTimeout', self.config_ini,'SITE','WEBDRIVER_TIMEOUT',int)

        # 商品タグCSS名
        super().setConfigValue('ItemTagName', self.config_ini,'SITE','ITEM_TAG_NAME',str)

        # 指定されたエレメントがDOMに発生するまで待機する
        super().setConfigValue('DelayWaitElement', self.config_ini,'SITE','DELAY_WAIT_ELEMENT',str)
                
        # Chrome-WebDriverパス(Windows)
        super().setConfigValue('chrome.WebDriverPathWin', self.config_ini,'WEBDRIVER-CHROME','CHR_WEBDRIVER_PATH_WIN',str)

        # Chrome-WebDriverパス(Linux)
        super().setConfigValue('chrome.WebDriverPathLinux', self.config_ini,'WEBDRIVER-CHROME','CHR_WEBDRIVER_PATH_LINUX',str)

        # Chrome-WebDriverパス(Mac)
        super().setConfigValue('chrome.WebDriverPathMac', self.config_ini,'WEBDRIVER-CHROME','CHR_WEBDRIVER_PATH_MAC',str)

        # Chrome-WebDriverログ出力先パス
        super().setConfigValue('chrome.WebDriverLogPath', self.config_ini,'WEBDRIVER-CHROME','CHR_WEBDRIVER_LOGPATH',str)
    
        # Firefox-WebDriverパス(Windows)
        super().setConfigValue('firefox.WebDriverPathWin', self.config_ini,'WEBDRIVER-FIREFOX','FOX_WEBDRIVER_PATH_WIN',str)

        # Firefox-WebDriverパス(Linux)
        super().setConfigValue('firefox.WebDriverPathLinux', self.config_ini,'WEBDRIVER-FIREFOX','FOX_WEBDRIVER_PATH_LINUX',str)

        # Firefox-WebDriverパス(Mac)
        super().setConfigValue('firefox.WebDriverPathMac', self.config_ini,'WEBDRIVER-FIREFOX','FOX_WEBDRIVER_PATH_MAC',str)

        # Firefox-WebDriverログ出力先パス
        super().setConfigValue('firefox.WebDriverLogPath', self.config_ini,'WEBDRIVER-FIREFOX','FOX_WEBDRIVER_LOGPATH',str)
