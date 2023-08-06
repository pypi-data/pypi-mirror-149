class scrapingerException:

    """
    Scrapinger例外クラス
    """
    
    class scrapingTypeErrorException(Exception):

        """
        スクレイピングタイプ指定例外
        """

        def __init__(self):

            """
            コンストラクタ
            """

            pass

        def __str__(self):
            
            """
            例外をプリントした時に出力する文字列
            """

            return "A function that can't be called with the specified scraping type"
        
    class resultDataGenerateError(Exception):

        """
        検索結果生成時例外
        """

        def __init__(self):

            """
            コンストラクタ
            """

            pass

        def __str__(self):
            
            """
            例外をプリントした時に出力する文字列
            """

            return "Failed to generate search dictionary"
            