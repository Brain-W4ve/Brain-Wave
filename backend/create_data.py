"""Para crear nuestro dataset teenemos que hacer lo siguiente:
    1) Meter un median filter
    2) Dividir la info en segmentos de 1 min (blobs)
    3) Por cada minuto checar el etiquetado y ver si es crisis o no, por ejemplo:
    si tenemos del min 1 al 2 que tiene crisis entonces es un 1
"""


import pandas as pd
import json
import numpy as np

def process_excel(file_path, segment_duration=60):
    data = {}

    xls = pd.ExcelFile(file_path)

    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)

        seizure_start_times = df['Inicio'].to_numpy()
        seizure_end_times = df['Fin'].to_numpy()

        total_duration = 360 * 60

        segments = []
        for start in range(0, total_duration, segment_duration):
            end = start + segment_duration
            label = 0

            for s_start, s_end in zip(seizure_start_times, seizure_end_times):
                if start < s_end and end >s_start:
                    label = 1
                    break

            segments.append({"start": start, "end": end, "label": label})

        data[sheet_name] = segments

    return data


def main():
    excel_file = "./register_data/EEG_Timestamps.xlsx"
    output_json = "./register_data/labeled_segments.json"

    labeled_data = process_excel(excel_file)

    with open(output_json, "w") as f:
        json.dump(labeled_data, f, indent=4)
    
    print(f"Labeled data saved to: {output_json}")


if __name__ == "__main__":
    main()