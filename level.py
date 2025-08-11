import os
import django
import re
import fitz  # PyMuPDF
from datetime import datetime
from django.db import transaction

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'water.settings')
django.setup()

from members.models import GroundwaterPlace, GroundwaterData

PDF_PATH = '/Users/kavishmalik/Desktop/water/pdfs/level.pdf'

# Timestamps (most recent first)
TIMESTAMPS = [
    ("2023-01-01", "2023/Jan"),
    ("2022-11-01", "2022/Nov"),
    ("2022-08-01", "2022/Aug"),
    ("2022-06-01", "2022/Jun"),
]

from collections import defaultdict

def extract_karnal_data():
    doc = fitz.open(PDF_PATH)
    data_rows = []

    print("\n📄 Scanning PDF Pages 68–98...\n")

    for page_num in range(67, 98):  # Page numbers are 0-indexed
        page = doc.load_page(page_num)
        words = page.get_text("words")  # returns: [x0, y0, x1, y1, "word", block_no, line_no, word_no]
        lines_by_y = defaultdict(list)

        for w in words:
            y = round(w[1], 1)  # use y0 rounded to 0.1 to group by line
            lines_by_y[y].append((w[0], w[4]))  # (x0, word)

        for y in sorted(lines_by_y):
            line = [word for _, word in sorted(lines_by_y[y])]
            line_str = " ".join(line)

            if "KARNAL" not in [w.upper() for w in line]:
                continue  # Only lines with district Karnal

            try:
                sl_no = int(line[0])
            except:
                continue

            try:
                k_index = line.index("KARNAL")
                location_raw = line[k_index + 1]
                values = line[k_index + 2:]
            except:
                continue

            location_clean = re.sub(r'-\s*PZ', '', location_raw, flags=re.IGNORECASE).strip()

            depth, sample_date = None, None
            for i in range(min(len(values), len(TIMESTAMPS)) - 1, -1, -1):
                try:
                    depth = float(values[i])
                    sample_date = datetime.strptime(TIMESTAMPS[i][0], "%Y-%m-%d").date()
                    break
                except:
                    continue

            if depth is not None:
                print(f"✅ {location_clean} | {depth} m | {sample_date}")
                data_rows.append({
                    'name': location_clean,
                    'district': 'Karnal',
                    'type': 'village',
                    'depth': depth,
                    'sample_date': sample_date
                })

    print(f"\n✅ Found {len(data_rows)} valid Karnal entries.")
    return data_rows


@transaction.atomic
def upload_groundwater_levels():
    entries = extract_karnal_data()
    count = 0

    # 🚨 Delete previous water level entries for Karnal
    GroundwaterData.objects.filter(
        place__district='Karnal',
        parameter='Water Level'
    ).delete()
    print("🧹 Deleted previous 'Water Level' entries for Karnal.")

    for entry in entries:
        place, _ = GroundwaterPlace.objects.get_or_create(
            name=entry['name'],
            district=entry['district'],
            defaults={'type': entry['type']}
        )

        GroundwaterData.objects.create(
            place=place,
            parameter='Water Level',
            value=entry['depth'],
            unit='m bgl',
            status='',
            sample_date=entry['sample_date']
        )
        count += 1

    print(f"\n✅ Uploaded {count} groundwater level entries for KARNAL.")


if __name__ == '__main__':
    upload_groundwater_levels()
