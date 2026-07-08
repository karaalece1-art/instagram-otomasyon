# Instagram Otomatik Paylaşım (Ücretsiz)

Sen düzenli olarak `content/queue/` klasörüne görsel/video atarsın,
otomasyon her gün sırayla birini alıp Instagram'a paylaşır. Herhangi bir
ücretli API kullanılmaz.

## Akış

```
content/queue/    -> Senin görsel/video attığın klasör (+ opsiyonel caption .txt)
content/posted/   -> Paylaşılanların otomatik taşındığı klasör
queue_manager.py  -> Sıradaki dosyayı ve caption'ı bulur
instagram_poster.py -> Instagram Graph API ile paylaşır (görsel + video/reels destekli)
main.py           -> Hepsini birleştirir
.github/workflows/daily_post.yml -> Günlük otomatik çalıştırma
```

## Nasıl kullanılır (senin tarafında)

1. Paylaşmak istediğin görsel/videoyu `content/queue/` klasörüne at.
   Dosya adını tarih ile başlatman sıralamayı garantiler, örnek:
   ```
   content/queue/2026-07-10_gorsel1.jpg
   content/queue/2026-07-10_gorsel1.txt   <- (opsiyonel) caption metni
   content/queue/2026-07-12_video1.mp4
   ```
2. Değişikliği reposuna push et (GitHub masaüstü uygulaması, web arayüzü
   veya git komutlarıyla yapabilirsin — hepsi ücretsiz).
3. Otomasyon her gün belirlenen saatte çalışır, sıradaki dosyayı paylaşır
   ve `content/posted/` klasörüne taşır. Böylece her gün uğraşman gerekmez,
   sen sadece ara sıra kuyruğu doldurursun.

Caption eklemezsen, gönderi metinsiz (sadece görsel/video) paylaşılır.

## Kurulum (bir kere yapılır)

### 1. Repo ayarı
- Bu klasörü bir **GitHub reposuna** yükle.
- Repo **PUBLIC** olmalı. Sebep: Instagram'a görseli/videoyu göndermek için
  herkese açık bir link gerekiyor; bunu GitHub'ın ücretsiz "raw dosya"
  linkiyle sağlıyoruz (ekstra barındırma servisi gerekmez). Repo private
  olursa bu link çalışmaz.
  > Not: Bu, queue/posted klasöründeki dosyaların link bilen herkes
  > tarafından görülebileceği anlamına gelir (zaten Instagram'da
  > paylaşacağın içerikler, ekstra hassasiyet gerektirmiyorsa sorun olmaz).

### 2. Instagram / Meta tarafı
1. Instagram hesabının **Business veya Creator** hesabı olduğundan emin ol.
2. Instagram hesabını bir **Facebook Sayfası**na bağla.
3. https://developers.facebook.com üzerinden bir **App** oluştur.
4. App'e **Instagram Graph API** ürününü ekle.
5. Gerekli izinleri iste: `instagram_basic`, `instagram_content_publish`,
   `pages_show_list`, `pages_read_engagement`.
6. Bir **User Access Token** al, sonra **uzun ömürlü token**'a çevir
   (~60 gün geçerli).
7. `IG_BUSINESS_ACCOUNT_ID`'yi bulmak için:
   `GET /me/accounts` -> Sayfa ID -> `GET /{page-id}?fields=instagram_business_account`

> Token 60 günde bir yenilenmeli, yoksa otomasyon hata verir.

### 3. GitHub Secrets
Reponun **Settings > Secrets and variables > Actions** kısmına ekle:

| Secret adı | Açıklama |
|---|---|
| `IG_ACCESS_TOKEN` | Uzun ömürlü Meta erişim token'ı |
| `IG_BUSINESS_ACCOUNT_ID` | Instagram Business hesap ID'si |

Bu iki secret dışında hiçbir ücretli API anahtarı gerekmiyor.

### 4. Zamanlama
`.github/workflows/daily_post.yml` içindeki cron ifadesini istediğin saate
göre düzenle. Repo'ya push ettiğinde GitHub Actions otomatik başlar.

### 5. Yerel test (opsiyonel)
```bash
pip install -r requirements.txt
export IG_ACCESS_TOKEN=...
export IG_BUSINESS_ACCOUNT_ID=...
export GITHUB_REPOSITORY=kullanici-adin/repo-adin
export GITHUB_REF_NAME=main
python main.py
```

## Maliyet özeti
- **Claude API / görsel üretim API'si** → Kullanılmıyor, maliyet yok.
- **Instagram Graph API** → Ücretsiz.
- **GitHub (public repo + Actions)** → Ücretsiz.

Tek "maliyetin" kendi zamanın: ara sıra `content/queue/` klasörünü
görsel/video ile doldurmak.

## Dikkat edilmesi gerekenler
- Kuyruk boşsa otomasyon o gün hiçbir şey paylaşmaz, hata da vermez.
- Video paylaşımları Instagram tarafında "Reels" olarak işlenir; işlenme
  süresi görsele göre daha uzun sürebilir (script bunu otomatik bekler).
- Instagram'ın otomasyon/spam politikalarına dikkat et; günde 1 paylaşım
  makul bir başlangıçtır.
