"""
queue_manager.py
------------------
content/queue/ klasöründeki dosyaları tarar, sıradaki (en eski/ilk sıradaki)
görsel veya videoyu bulur. Aynı isimde bir .txt dosyası varsa onu caption
olarak kullanır.

Dosya adlarını tarih ile başlatmanız sıralamayı kolaylaştırır, örn:
    2026-07-10_gorsel1.jpg
    2026-07-10_gorsel1.txt   (opsiyonel caption)
"""

import os
import shutil

QUEUE_DIR = "content/queue"
POSTED_DIR = "content/posted"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {".mp4", ".mov"}


def get_next_item():
    """
    Sıradaki medya dosyasını döndürür.

    Returns:
        dict {"path": str, "type": "image"|"video", "caption": str} veya None
    """
    if not os.path.isdir(QUEUE_DIR):
        return None

    files = sorted(os.listdir(QUEUE_DIR))
    media_files = [
        f for f in files
        if os.path.splitext(f)[1].lower() in (IMAGE_EXTENSIONS | VIDEO_EXTENSIONS)
    ]

    if not media_files:
        return None

    filename = media_files[0]
    ext = os.path.splitext(filename)[1].lower()
    media_type = "image" if ext in IMAGE_EXTENSIONS else "video"

    caption_path = os.path.join(QUEUE_DIR, os.path.splitext(filename)[0] + ".txt")
    caption = ""
    if os.path.exists(caption_path):
        with open(caption_path, "r", encoding="utf-8") as f:
            caption = f.read().strip()

    return {
        "path": os.path.join(QUEUE_DIR, filename),
        "filename": filename,
        "type": media_type,
        "caption": caption,
    }


def mark_as_posted(item: dict):
    """Paylaşılan dosyayı (ve varsa caption dosyasını) posted/ klasörüne taşır."""
    os.makedirs(POSTED_DIR, exist_ok=True)

    shutil.move(item["path"], os.path.join(POSTED_DIR, item["filename"]))

    caption_filename = os.path.splitext(item["filename"])[0] + ".txt"
    caption_path = os.path.join(QUEUE_DIR, caption_filename)
    if os.path.exists(caption_path):
        shutil.move(caption_path, os.path.join(POSTED_DIR, caption_filename))


if __name__ == "__main__":
    next_item = get_next_item()
    print(next_item)
