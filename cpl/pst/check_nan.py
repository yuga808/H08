import numpy as np
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python check_nan.py <input_file>")
        return

    input_path = sys.argv[1]

    try:
        data = np.fromfile(input_path, dtype=np.float32)
        total = data.size
        nan_count = np.isnan(data).sum()
        ratio = nan_count / total * 100
        print(f"[INFO] Total values: {total}")
        print(f"[INFO] NaN count   : {nan_count}")
        print(f"[INFO] NaN ratio   : {ratio:.6f}%")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()

