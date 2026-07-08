"""
instagram_poster.py
---------------------
Instagram Graph API kullanarak, halka açık bir görsel/video URL'i ve caption
ile Instagram Business/Creator hesabına gönderi paylaşır.

ÖNEMLİ: Instagram Graph API, medyayı senden dosya olarak almaz; herkese açık
(internetten erişilebilir) bir URL ister. Bu proje, medyayı repo'daki
content/queue/ klasöründen GitHub'ın kendi "raw" linkiyle sunar
(bkz. main.py -> build_public_url), böylece ekstra bir barındırma servisine
gerek kalmaz.

Ortam değişkenleri:
    IG_ACCESS_TOKEN        -> Uzun ömürlü Meta erişim token'ı
    IG_BUSINESS_ACCOUNT_ID -> Instagram Business hesabının ID'si
"""

import os
import time
import requests

GRAPH_API_VERSION = "v21.0"
# NOT: "Instagram Login" akışıyla alınan token'lar graph.instagram.com üzerinden
# çalışır (graph.facebook.com değil). Facebook Sayfası gerekmez, IG_BUSINESS_ACCOUNT_ID
# doğrudan Instagram User ID'dir.
BASE_URL = f"https://graph.instagram.com/{GRAPH_API_VERSION}"


def _ig_user_id():
    return os.environ["IG_BUSINESS_ACCOUNT_ID"]


def _access_token():
    return os.environ["IG_ACCESS_TOKEN"]


def create_media_container(
    media_url: str, caption: str, media_type: str = "image", alt_text: str = ""
) -> str:
    """
    Adım 1: Görsel veya video ve caption ile bir 'media container' oluşturur.

    media_type: "image" veya "video"
    alt_text: (opsiyonel) erişilebilirlik için ekran okuyucu açıklaması
    """
    data = {
        "caption": caption,
        "access_token": _access_token(),
    }

    if alt_text:
        data["alt_text"] = alt_text

    if media_type == "video":
        data["media_type"] = "REELS"  # Feed videoları da Reels olarak yayınlanır
        data["video_url"] = media_url
    else:
        data["image_url"] = media_url

    resp = requests.post(f"{BASE_URL}/{_ig_user_id()}/media", data=data, timeout=30)
    resp.raise_for_status()
    return resp.json()["id"]


def wait_until_ready(container_id: str, timeout_seconds: int = 300, poll_seconds: int = 10):
    """
    Video containerları hemen hazır olmaz; Meta'nın işlemesini bekler.
    Görseller genelde anında hazırdır ama yine de kontrol edilir.
    """
    elapsed = 0
    while elapsed < timeout_seconds:
        resp = requests.get(
            f"{BASE_URL}/{container_id}",
            params={"fields": "status_code", "access_token": _access_token()},
            timeout=30,
        )
        resp.raise_for_status()
        status = resp.json().get("status_code")

        if status == "FINISHED":
            return
        if status == "ERROR":
            raise RuntimeError(f"Medya işlenemedi (container: {container_id})")

        time.sleep(poll_seconds)
        elapsed += poll_seconds

    raise TimeoutError(f"Medya işlenmesi {timeout_seconds} saniyede tamamlanmadı.")


def publish_media(container_id: str) -> dict:
    """Adım 2: Oluşturulan container'ı yayınlar."""
    resp = requests.post(
        f"{BASE_URL}/{_ig_user_id()}/media_publish",
        data={"creation_id": container_id, "access_token": _access_token()},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def post_to_instagram(
    media_url: str, caption: str, media_type: str = "image", alt_text: str = ""
) -> dict:
    """Tam akış: container oluştur -> hazır olmasını bekle -> yayınla."""
    container_id = create_media_container(media_url, caption, media_type=media_type, alt_text=alt_text)
    wait_until_ready(container_id)
    return publish_media(container_id)


if __name__ == "__main__":
    # Test amaçlı örnek çağrı (gerçek, herkese açık bir görsel URL'i gerekir)
    test_url = "https://example.com/gorsel.jpg"
    test_caption = "Test gönderisi 🚀 #test"
    print(post_to_instagram(test_url, test_caption, media_type="image"))
