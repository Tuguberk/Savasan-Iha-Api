# Teknofest 2021 Savaşan İha Api Sistemi

Teknofest'in yayınlamış olduğu [Haberleşme Dökümanı](https://teknofest.org/upload/0033aaf090489e512c554d7a565470cb.pdf)'nda verilen standartlara uygun api istemcisi. 

***Proje geliştirme aşamasındadır!***

### Bilgilendirme
***Bu kodları geliştirme sürecinde kullanan tüm teknofest takımlarından [akbulut.tugberk@gmail.com]() adresine mail atmalarını rica ediyorum. Kodlar tamamen halka açık ve ücretsizdir. Sadece faydamın dokunduğu takımları tanımak istiyorum. Bir merhaba demekten çekinmeyin*** :)
## Kullanım

1. `pip3 install --user fastapi uvicorn`
2. `uvicorn server:app --reload`
3. [http://127.0.0.1:8000]()
4. [http://127.0.0.1:8000/docs]()

## ToDo List

- [x] Oturum Açma
- [x] Oturum Kapama
- [x] Hata ve onay kodlarının kontrolü
- [x] Zaman farklarının hesaplanarak gönderilmesi
- [x] Takımlardan toplanan verilerin kaydedilmesi
- [ ] Gönderilen takım verilerin gerçekçi olması
- [ ] Client kütüphanesi
- [ ] kilitlenme eklenecek
- [ ] QR kod eklenecek
- [ ] Optimizasyon yapılacak

## Eklenenler
- Kullanıcıları listeleme
- json dosyasından kullanıcı kontrolü
## Geliştirme
Geliştirme önerilerinizi için Issues başlığından bana iletebilirsiniz. Repoyu forklamaktan çekinmeyin. 

