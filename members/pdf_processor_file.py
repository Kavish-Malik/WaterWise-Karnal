# members/pdf_processor.py

import re, fitz
from datetime import datetime
from collections import defaultdict
from django.db import transaction
from .models import GroundwaterPlace, GroundwaterData

TIMESTAMPS = [
    ("2023-01-01", "2023/Jan"),
    ("2022-11-01", "2022/Nov"),
    ("2022-08-01", "2022/Aug"),
    ("2022-06-01", "2022/Jun"),
]

def process_pdf_file(file_path):
    doc = fitz.open(file_path)
    data_rows = []

    for page_num in range(67, 98):
        page = doc.load_page(page_num)
        words = page.get_text("words")
        lines_by_y = defaultdict(list)

        for w in words:
            y = round(w[1], 1)
            lines_by_y[y].append((w[0], w[4]))

        for y in sorted(lines_by_y):
            line = [word for _, word in sorted(lines_by_y[y])]
            if "KARNAL" not in [w.upper() for w in line]: continue
            try: sl_no = int(line[0])
            except: continue
            try:
                k_index = line.index("KARNAL")
                location_raw = line[k_index + 1]
                values = line[k_index + 2:]
            except: continue

            location_clean = re.sub(r'-\s*PZ', '', location_raw, flags=re.IGNORECASE).strip()
            depth, sample_date = None, None
            for i in range(min(len(values), len(TIMESTAMPS)) - 1, -1, -1):
                try:
                    depth = float(values[i])
                    sample_date = datetime.strptime(TIMESTAMPS[i][0], "%Y-%m-%d").date()
                    break
                except: continue

            if depth is not None:
                data_rows.append({
                    'name': location_clean,
                    'district': 'Karnal',
                    'type': 'village',
                    'depth': depth,
                    'sample_date': sample_date
                })

    with transaction.atomic():
        GroundwaterData.objects.filter(
            place__district='Karnal',
            parameter='Water Level'
        ).delete()

        count = 0
        for entry in data_rows:
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
    return count
