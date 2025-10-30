# src/data/preprocess_cv_lite.py
"""
Process images and save lightweight CV metadata and small embeddings.

Outputs:
  data/dataset/cv_metadata_lite.csv
  data/dataset/embeddings/*.pkl  (face embedding and tiny visual embedding per image)
Usage:
  python preprocess_cv_lite.py --meta data/dataset/metadata.csv --out data/dataset
"""
import os, argparse, pandas as pd
from tqdm import tqdm
from PIL import Image
import numpy as np
import joblib
import face_recognition
from ultralytics import YOLO
import pytesseract

def tiny_visual_embedding(img_path):
    im = Image.open(img_path).convert('L').resize((64,64))
    arr = np.asarray(im).astype('float32') / 255.0
    return arr.flatten()[:4096]

def process(meta_csv, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    emb_dir = os.path.join(out_dir, "embeddings")
    os.makedirs(emb_dir, exist_ok=True)
    meta = pd.read_csv(meta_csv)
    yolo = YOLO('yolov8n.pt')  # nano model, CPU-friendly
    rows=[]
    for _, r in tqdm(meta.iterrows(), total=len(meta)):
        imgfile = r.get('file') or r.get('filepath') or None
        if not imgfile or not os.path.exists(imgfile):
            # if file doesn't exist, skip
            rows.append({'id': r['id'], 'file': None, 'num_faces':0, 'yolo_labels':"", 'ocr':""})
            continue
        # face embedding
        try:
            img = face_recognition.load_image_file(imgfile)
            encs = face_recognition.face_encodings(img)
            if len(encs)>0:
                face_emb = encs[0]
                joblib.dump(face_emb, os.path.join(emb_dir, f"{r['id']}_face.pkl"))
                num_faces = len(encs)
            else:
                num_faces = 0
        except Exception as e:
            num_faces = 0
        # yolo labels
        try:
            res = yolo.predict(source=imgfile, imgsz=640, device='cpu', conf=0.35, verbose=False)
            labels=set()
            for r0 in res:
                for box in r0.boxes.data.tolist():
                    labels.add(int(box[5]))
            ylabels = ",".join(map(str, labels))
        except Exception as e:
            ylabels = ""
        # tiny visual embedding
        try:
            vis = tiny_visual_embedding(imgfile)
            joblib.dump(vis, os.path.join(emb_dir, f"{r['id']}_vis.pkl"))
        except:
            pass
        # OCR
        try:
            txt = pytesseract.image_to_string(Image.open(imgfile))
            txt = txt[:300]
        except:
            txt = ""
        rows.append({'id': r['id'], 'file': imgfile, 'num_faces': num_faces, 'yolo_labels': ylabels, 'ocr': txt})
    out_csv = os.path.join(out_dir, "cv_metadata_lite.csv")
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    print("Wrote", out_csv)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--meta", default="data/dataset/metadata.csv")
    p.add_argument("--out", default="data/dataset")
    args = p.parse_args()
    process(args.meta, args.out)
