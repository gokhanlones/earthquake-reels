import os
import requests
import time

IG_TOKEN = os.environ["IG_TOKEN"]
IG_USER_ID = os.environ["IG_USER_ID"]

# 1. Görseli geçici hosting'e yükle
print("Görsel yükleniyor...")
with open("output.jpg", "rb") as f:
    upload_res = requests.post(
        "https://0x0.st",
        files={"file": f}
    )

print("Upload status:", upload_res.status_code)
image_url = upload_res.text.strip()
print("Görsel URL:", image_url)

# 2. Instagram container oluştur
container_res = requests.post(
    f"https://graph.instagram.com/v21.0/{IG_USER_ID}/media",
    data={
        "image_url": image_url,
        "caption": "🌍 Earthquake Alert\n\n#earthquake #deprem #seismic",
        "access_token": IG_TOKEN
    }
)
print("Container:", container_res.json())
container_id = container_res.json().get("id")

if not container_id:
    print("Container hatası!")
    exit(1)

# 3. Yayınla
time.sleep(5)
publish_res = requests.post(
    f"https://graph.instagram.com/v21.0/{IG_USER_ID}/media_publish",
    data={
        "creation_id": container_id,
        "access_token": IG_TOKEN
    }
)
print("Publish:", publish_res.json())

if publish_res.json().get("id"):
    print("✅ Paylaşıldı!")
else:
    print("❌ Hata!")
    exit(1)
