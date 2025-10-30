# src/data/download_images_from_urls.py
"""
Download images from a CSV with columns: id,url
Usage:
    python download_images_from_urls.py --csv image_urls.csv --out data/images --max 200
"""
import os
import argparse
import csv
import requests
from tqdm import tqdm

def download(csv_path, out_dir, max_images=None):
    os.makedirs(out_dir, exist_ok=True)
    count=0
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader):
            if max_images and count >= max_images:
                break
            img_id = row.get('id') or row.get('image_id') or str(count)
            url = row.get('url') or row.get('image_url')
            if not url:
                continue
            fname = os.path.join(out_dir, f"{img_id}.jpg")
            if os.path.exists(fname):
                count += 1
                continue
            try:
                r = requests.get(url, timeout=15)
                if r.status_code == 200:
                    with open(fname, 'wb') as out:
                        out.write(r.content)
                    count += 1
            except Exception as e:
                # skip
                continue
    print(f"Downloaded {count} images to {out_dir}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    p.add_argument("--out", default="data/images")
    p.add_argument("--max", type=int, default=None)
    args = p.parse_args()
    download(args.csv, args.out, args.max)
