# OneWordSearch

`OneWordSearch`, belirli bir sorguya karşılık gelen Wikipedia sayfalarını bulmak ve bu sayfalardan belirli bir sayıda cümle içeren paragrafları çıkarmak için tasarlanmış bir Python kütüphanesidir. Bu araç, özellikle dil ve bölge seçimini destekleyerek Wikipedia'da çok yönlü aramalar yapmayı kolaylaştırır.

## Özellikler

- **Wikipedia'da Arama**: Belirli bir sorguya karşılık gelen Wikipedia sayfasını otomatik olarak bulur ve sayfanın bağlantısını döndürür.
- **Paragraf Çıkarma**: Bulunan Wikipedia sayfasındaki paragraflardan belirli bir sayıda cümle içerenleri çıkarır ve döndürür.
- **Dil ve Bölge Desteği**: Wikipedia üzerinde yapılan aramalar için dil (`lang`) ve bölge (`region`) seçeneği sunar. Varsayılan olarak Türkçe (`tr`) ve Türkiye bölgesi (`tr`) kullanılmaktadır.
- **Özelleştirilebilir Başlık Bilgileri**: HTTP isteklerinde kullanılacak başlık bilgileri (`headers`) özelleştirilebilir, bu sayede isteklerin Wikipedia tarafından doğru şekilde işlenmesi sağlanır.

## Kurulum

Kütüphaneyi kullanmadan önce gerekli bağımlılıkları yüklemeniz gerekir:

```bash
pip install beautifulsoup4 requests googlesearch-python
