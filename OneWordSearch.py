from bs4 import BeautifulSoup as BS4
from googlesearch import search
from requests import get, RequestException
from typing import Optional
from logging import basicConfig , INFO , warning ,error

class OneWordSearch:
    """
    OneWordSearch sınıfı, verilen bir sorguya karşılık gelen Wikipedia sayfasını bulmak
    ve bu sayfadan belirli bir sayıda cümle içeren paragrafları çıkarmak için kullanılan bir araçtır.

    Bu sınıf, Wikipedia'da belirli bir sorgu ile arama yapar, ilgili sayfanın bağlantısını alır ve bu sayfadan
    en az belirtilen sayıda cümle içeren paragrafları çıkartır. Sınıf, Wikipedia'nın bir dil seçeneğinde
    çalışabilir ve varsayılan olarak Türkçe dil seçeneğini kullanır.

    Özellikler:
    - headers: Wikipedia'ya yapılan HTTP istekleri için kullanılan başlık bilgilerini içerir.
    - min_sentences: Her arama için minimum cümle sayısını belirler.
    - lang: Wikipedia araması yapılacak dil, varsayılan olarak 'tr' yani Türkçe.
    - region: Aramanın yapılacağı bölge, varsayılan olarak 'tr' yani Türkiye.

    Metodlar:
    - __init__(): Sınıfın başlatıcısı, User-Agent başlığını, minimum cümle sayısını, dil ve bölge ayarlarını belirler.
    - get_wikipedia_link(wiki_query:str): Verilen sorgu için Wikipedia'da arama yapar
      ve ilgili sayfanın bağlantısını döndürür. Eğer sayfa bulunamazsa None döner.
    - get_paragraphs(link:str): Verilen Wikipedia sayfası bağlantısından istenilen
      minimum cümle sayısına sahip paragrafları çıkarır. Eğer bağlantı geçersizse veya hata oluşursa None döner.
    - search_query(query:str): Verilen sorguyu Wikipedia'da arar, ilgili sayfanın bağlantısını bulur
      ve bu sayfadan en az belirtilen sayıda cümle içeren paragrafları döndürür. İçerik bulunamazsa hata mesajı döner.
    """

    def __init__(self, 
                 headers: dict = {"User-Agent": "Mozilla/5.0"}, 
                 min_sentences: int = 10,
                 lang: str = "tr",
                 region: str = "tr"):
        """
        OneWordSearch sınıfının başlatıcısıdır.

        Parametreler:
        - headers (dict): Wikipedia'ya yapılacak HTTP isteklerinde kullanılacak başlık bilgileri. Varsayılan olarak
            User-Agent başlığı "Mozilla/5.0" değerini içerir. Başlık bilgileri, isteğin doğru şekilde işlenmesini sağlamak için
            HTTP isteklerinde kullanılır.
        - min_sentences (int): Her arama için minimum cümle sayısı, varsayılan olarak 10.
        - lang (str): Wikipedia araması yapılacak dil, varsayılan olarak 'tr' yani Türkçe.
        - region (str): Aramanın yapılacağı bölge, varsayılan olarak 'tr' yani Türkiye.
        """
        self.headers = headers
        self.min_sentences = min_sentences
        self.lang = lang
        self.region = region
        basicConfig(level=INFO)

    def get_wikipedia_link(self, wiki_query: str) -> Optional[str]:
        """
        Verilen sorgu için Wikipedia üzerinde arama yapar ve ilgili Wikipedia sayfasının bağlantısını döndürür.

        :param wiki_query: Aranacak kelime veya cümle.
        :return: Wikipedia sayfası bağlantısı veya None (Eğer sayfa bulunamazsa).
        """
        try:
            results = search(f"{wiki_query} site:{self.lang}.wikipedia.org", region=self.region)
            for link in results:
                if f'{self.lang}.wikipedia.org' in link:
                    return link
        except Exception as e:
            error(f"Error in searching Wikipedia link: {e}")
        return None

    def get_paragraphs(self, link: str) -> Optional[str]:
        """
        Verilen Wikipedia sayfası bağlantısından istenilen minimum cümle sayısına sahip paragrafları döndürür.

        :param link: Wikipedia sayfası bağlantısı.
        :return: İstenen sayıda cümle içeren paragraflar veya None (Eğer bağlantı geçersizse veya hata oluşursa).
        """
        if not link:
            warning("No link provided.")
            return None
        
        try:
            response = get(link, headers=self.headers)
            response.raise_for_status()
            paragraphs = BS4(response.content, "html.parser").find("div", id="bodyContent").find_all("p")
            content, sentence_count = "", 0
            for p in paragraphs:
                paragraph = p.text.strip()
                if paragraph:
                    content += paragraph + "\n" 
                    sentence_count += len(paragraph.split("."))  
                    if sentence_count >= self.min_sentences:
                        break
            return content if content else None
        except RequestException as e:
            error(f"Error in fetching Wikipedia page: {e}")
            return None

    def search_query(self, query: str) -> tuple[str, Optional[str]]:
        """
        Verilen sorguyu Wikipedia'da arar, ilgili sayfanın bağlantısını bulur ve 
        bu sayfadan en az belirtilen sayıda cümle içeren paragrafları döndürür.

        metod hem içeriği (paragrafları) hem de Wikipedia sayfasının bağlantısını 
        bir tuple olarak döndürür. Eğer içerik bulunamazsa, bir hata mesajı ve None döner.

        :param query: Aranacak kelime veya cümle. Wikipedia'da bu sorguya karşılık 
                    gelen sayfa bulunmaya çalışılır.
        :return: Bir tuple olarak (içerik, sayfa bağlantısı) döner.
        """
        wiki_link = self.get_wikipedia_link(query)
        content = self.get_paragraphs(wiki_link)
        
        if content:
            return content, wiki_link
        else:
            return "Aranan içerik Wikipedia kaynağında yok.", wiki_link
