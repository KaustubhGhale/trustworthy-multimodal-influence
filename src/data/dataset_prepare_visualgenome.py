# src/data/dataset_prepare_visualgenome.py
"""
Prepare dataset metadata.

Two modes:
1) If you already have Visual Genome annotation file `visual_genome_image_data.json`
   in the same folder: the script will parse it and download required images.
2) If you have a local directory of images (data/images), it will just produce metadata.csv.

Outputs:
  data/dataset/metadata.csv  (columns: id, file, title, width, height, url)
Usage:
  python dataset_prepare_visualgenome.py --mode local --img_dir data/images
  OR
  python dataset_prepare_visualgenome.py --mode vg --vg_json path/to/image_data.json --out data/dataset
"""

import os, argparse, json, csv
from tqdm import tqdm

def prepare_from_local(img_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    rows=[]
    for fname in os.listdir(img_dir):
        if not fname.lower().endswith((".jpg",".jpeg",".png")):
            continue
        img_id = os.path.splitext(fname)[0]
        path = os.path.abspath(os.path.join(img_dir, fname))
        rows.append({'id': img_id, 'file': path, 'title': fname})
    # write CSV
    out_csv = os.path.join(out_dir, "metadata.csv")
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id','file','title'])
        writer.writeheader()
        for r in rows: writer.writerow(r)
    print("Wrote", out_csv, "with", len(rows), "rows")

def prepare_from_vg(vg_json_path, out_dir, img_dir=None, limit=None):
    """
    vg_json_path: path to Visual Genome image_data.json (list of dicts)
    Each item usually has: 'image_id', 'url', 'width', 'height', 'img_name'
    """
    os.makedirs(out_dir, exist_ok=True)
    rows=[]
    with open(vg_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for i, item in enumerate(tqdm(data)):
        if limit and i >= limit: break
        img_id = str(item.get('image_id') or item.get('img_name') or i)
        url = item.get('url')
        fname = None
        if img_dir:
            # expect image already downloaded with name image_id.jpg
            candidate = os.path.join(img_dir, f"{img_id}.jpg")
            if os.path.exists(candidate):
                fname = os.path.abspath(candidate)
        rows.append({'id': img_id, 'url': url, 'file': fname, 'width': item.get('width'), 'height': item.get('height')})
    out_csv = os.path.join(out_dir, "metadata.csv")
    import csv
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id','file','url','width','height'])
        writer.writeheader()
        for r in rows: writer.writerow(r)
    print("Wrote", out_csv, "with", len(rows), "rows")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=['local','vg'], default='local')
    p.add_argument("--img_dir", default="data/images")
    p.add_argument("--vg_json", default=None)
    p.add_argument("--out", default="data/dataset")
    p.add_argument("--limit", type=int, default=None)
    args = p.parse_args()
    if args.mode == 'local':
        prepare_from_local(args.img_dir, args.out)
    else:
        if not args.vg_json:
            print("Please provide --vg_json path (Visual Genome image_data.json)")
        else:
            prepare_from_vg(args.vg_json, args.out, args.img_dir, args.limit)
