import requests

API_KEY = 'AIzaSyCyAyCZrAQoTUc0Z6Z2dMwI547oWtHVav8'
CHANNEL_ID = 'UCefmzhGcyDHOE-wzoKy4egA'

url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={CHANNEL_ID}&key={API_KEY}'

print("Sedang mengetukk pintu server Youtube...")

# Mengirim kurir untuk mengambil data
respons = requests.get(url)

# Jika pintu berhasil dibuka (Status 200 = OK)
if respons.status_code == 200:
    data_mentah = respons.json()
    
    # Membongkar paket JSOn untuk mengambil angka subscirber dan view
    statistik = data_mentah['items'][0]['statistics']
    subsciber = statistik['subscriberCount']
    total_view = statistik['viewCount']
    video_count = statistik['videoCount']
    
    print('\n=== DATA BERHASIL DIAMBIL! ===')
    print(f'Total Subsciber  : {subsciber}')
    print(f'Total View       : {total_view}')
    print(f'Total Video      : {video_count}')
else:
    print(f'Gagal! Server membalas dengan kode: {respons.status_code}')

