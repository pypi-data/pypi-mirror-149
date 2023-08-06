from LibHanger.Library.uwGlobals import globalValues

class scrapingerGlobal(globalValues):
    
    def __init__(self):
        
        """
        コンストラクタ
        """
            
        # 基底側コンストラクタ呼び出し
        super().__init__()
        
        self.scrapingerConfig = None
        """ Scrapinger共通設定 """

# インスタンス生成(import時に実行される)
gv = scrapingerGlobal()