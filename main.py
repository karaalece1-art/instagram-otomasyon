"""
main.py
--------
Ücretsiz akış:
1. content/queue/ klasöründeki sıradaki görsel/videoyu bul
2. GitHub raw linkiyle herkese açık URL oluştur
3. Instagram'a paylaş
4. Dosyayı content/posted/ klasörüne taşı (tekrar paylaşılmasın diye)

Çalıştırma:
    python main.py
"""

import os
import sys

from queue_manager import get_next_item, mark_as_posted
from instagram_poster import post_to_instagram


def build_public_url(relative_path: str) -> str:
    """
    Repo içindeki bir dosyanın GitHub 'raw' linkini oluşturur.
    NOT: Bunun çalışması için repo PUBLIC olmalı (raw.githubusercontent.com
    private reponun dosyalarını token'sız servis edemez).
    """
    repo = os.environ["GITHUB_REPOSITORY"]  # GitHub Actions bunu otomatik sağlar, örn: "kullanici/repo"
    branch = os.environ.get("GITHUB_REF_NAME", "main")
    relative_path = relative_path.replace(os.sep, "/")
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{relative_path}"


def run():
    item = get_next_item()

    if item is None:
        print("Kuyrukta paylaşılacak yeni içerik yok. content/queue/ klasörüne dosya ekleyin.")
        sys.exit(0)

    print(f"Paylaşılacak dosya: {item['filename']} (tür: {item['type']})")

    public_url = build_public_url(item["path"])
    print(f"Public URL: {public_url}")

    caption = item["caption"] or ""

    result = post_to_instagram(public_url, caption, media_type=item["type"])
    print("Paylaşım tamamlandı:", result)

    mark_as_posted(item)
    print(f"'{item['filename']}' posted/ klasörüne taşındı.")


if __name__ == "__main__":
    run()
