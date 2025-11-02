import csv
import random

# ✅ Categories matching your project
categories = [
    "people meeting",
    "conference event",
    "crowded street",
    "cafe group",
    "team office",
    "university classroom",
    "friends gathering",
    "concert audience",
    "restaurant crowd",
    "public park group"
]

# ✅ Predefined image sources (free use)
pexels_base = "https://images.pexels.com/photos/"
unsplash_base = "https://images.unsplash.com/photo-"

# ✅ Sample image IDs (these exist publicly)
pexels_ids = [
    "3184287", "1181686", "1181353", "3184403", "1181681", "3183186",
    "776656", "1438072", "1858175", "1323592", "1640777", "207983", 
    "3184312", "2379004", "2774556", "1181716", "3789884", "977796",
    "2645547", "2584837", "3183178", "3075991", "1413653", "3775538",
    "1181391", "3184328", "1640778", "1181273", "3184291", "3183192"
]

unsplash_ids = [
    "1519389950473-47ba0277781c", "1522205418593-83de48d61c7c", "1494790108377-be9c29b29330",
    "1506794778202-cad84cf45f1d", "1504384308090-c894fdcc538d", "1515165562835-c4c1e0fa7e1e",
    "1517841905240-472988babdf9", "1504384308090-c894fdcc538d", "1551836022-d5d88e9218df",
    "1506744038136-46273834b3fb", "1526948128573-703ee1aeb6fa", "1507537297725-24a1c029d3ca"
]

# ✅ Generate a list of image URLs
urls = []
id_counter = 1

# Mix Pexels & Unsplash
for _ in range(50):  # repeat to generate ~500 entries
    for pid in random.sample(pexels_ids, len(pexels_ids)):
        urls.append((id_counter, f"{pexels_base}{pid}/pexels-photo-{pid}.jpeg"))
        id_counter += 1
    for uid in random.sample(unsplash_ids, len(unsplash_ids)):
        urls.append((id_counter, f"{unsplash_base}{uid}?auto=format&fit=crop&w=1200&q=80"))
        id_counter += 1
    if len(urls) >= 500:
        break

# ✅ Save as CSV
out_path = "data/image_urls.csv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "url"])
    writer.writerows(urls)

print(f"✅ Generated {len(urls)} image URLs at {out_path}")
