import random
import bioread
import numpy as np
import json 
from pathlib import Path

class U_Net:   
        
    def process(self, acq_file: Path) -> str:
        try:
            data = bioread.read(acq_file)
            
            eeg_signal = data.channels[0].data
            sampling_rate = data.channels[0].samples_per_second
            total_seconds = len(eeg_signal) / sampling_rate

            # simulate attack detection by randomly selecting some timestamps
            attack_count = min(3, max(1, int(total_seconds // 15)))  # Max 3 attacks, spaced out
            attack_timestamps = sorted(random.sample(range(int(total_seconds)), attack_count))

            attacks = []
            for t in attack_timestamps:
                duration = random.uniform(1.5, 3.0)
                attacks.append({
                    "start": round(t, 2),
                    "finish": round(min(t + duration, total_seconds), 2),
                    "name": "Seizure"
                })

            response = {
                "channels": [
                    {
                        "samplingRate": sampling_rate,
                        "data": eeg_signal.tolist(),
                        "attacks": attacks
                    }
                ]
            }

            processed_file = f"processed-{acq_file.name}"
            with open(processed_file, "w") as file:
                json.dump(response, file)
            
            return processed_file

        except Exception as e:
            print(f"Error processing EEG file: {e}")
            return {"error": str(e)}