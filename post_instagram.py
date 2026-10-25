import os
import requests
import base64

IG_TOKEN = os.environ["IG_TOKEN"]
IG_USER_ID = os.environ["IG_USER_ID"]

# Görseli base64'e çevir
with open("output.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

# 1. Adım: Container oluştur
container_url = f"https://graph.instagram.com/v21.0/{IG_USER_ID}/media"
container_res = requests.post(container_url, data={
    "image_url": "data:image/jpeg;base64," + image_data,
    "caption": "🌍 Earthquake Alert\n\n#earthquake #deprem #seismic",
    "access_token": IG_TOKEN
})

print("Container response:", container_res.json())
container_id = container_res.json().get("id")

if not container_id:
    print("Container oluşturulamadı!")
    exit(1)

# 2. Adım: Yayınla
publish_url = f"https://graph.instagram.com/v21.0/{IG_USER_ID}/media_publish"
publish_res = requests.post(publish_url, data={
    "creation_id": container_id,
    "access_token": IG_TOKEN
})

print("Publish response:", publish_res.json())
