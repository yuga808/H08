import os
import requests

# 認証トークン（ISIMIPポータルから取得）
#auth_token = "your_api_token_here"

# ダウンロード対象のURLリスト
data_urls = [
    "https://data.isimip.org/ISIMIP3b/water/global/ssp370_2015soc-from-histsoc_default/file1.nc",
    "https://data.isimip.org/ISIMIP3b/water/global/ssp370_2015soc-from-histsoc_default/file2.nc",
    # 必要なファイルのURLをリストに追加
]

# ダウンロード先ディレクトリ
download_dir = "../tmp"
os.makedirs(download_dir, exist_ok=True)

# ヘッダーに認証トークンを追加
#headers = {"Authorization": f"Bearer {auth_token}"}

# ダウンロード処理
for url in data_urls:
    file_name = os.path.basename(url)
    file_path = os.path.join(download_dir, file_name)

    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Downloaded: {file_path}")
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")

