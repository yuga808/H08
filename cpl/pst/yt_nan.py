import numpy as np
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python yt_nan.py <input_file> <output_file>")
        return

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    try:
        data = np.fromfile(input_path, dtype=np.float32)
        nan_count = np.isnan(data).sum()
        print(f"[INFO] NaNs detected: {nan_count}")
        data[np.isnan(data)] = 0.0
        data.astype(np.float32).tofile(output_path)
        print(f"[OK] Output saved to: {output_path}")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
