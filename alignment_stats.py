import argparse
import numpy as np
from pathlib import Path

def alignment_stats(xf_dir):
    """
    Parse one or more XF files containing transformation data for tilt-series images.
    Prints mean and std of dx and dy for each tilt and overall.

    :param Path xf_dir: Directory to XF files.
    :return: Tuple (xf_data, tilt_data)
    """
    xf_data = []  # List of [dx, dy] for all tilts in all files
    tilt_data = {}  # Dict: tilt index -> list of [dx, dy] for that tilt

    # Read the file(s)
    for file_path in xf_dir.glob('*.xf'):
        with open(file_path, 'r') as f:
            lines = f.readlines()

            # Extract TY and TX (last two columns)
            for i, line in enumerate(lines):
                parts = line.split()
                if len(parts) != 6:
                    raise ValueError(f"Invalid line format: {line.strip()}")
                
                dx, dy = map(float, parts[4:])
                xf_data.append([dx, dy])
                if i not in tilt_data:
                    tilt_data[i] = []
                tilt_data[i].append([dx, dy])

    # Calculate stats per tilt
    for i, data in tilt_data.items():
        arr = np.array(data)
        dx_mean = np.mean(arr[:, 0])
        dy_mean = np.mean(arr[:, 1])
        dx_std = np.std(arr[:, 0])
        dy_std = np.std(arr[:, 1])
        print(f"Tilt {i}:")
        print(f"  Mean: ({dx_mean}, {dy_mean})")
        print(f"  Std: ({dx_std}, {dy_std})")

    # Print avg and std of all tilts
    xf_arr = np.array(xf_data)
    print(f"Avg dx: {np.mean(xf_arr[:, 0])}, Avg dy: {np.mean(xf_arr[:, 1])}")
    print(f"Std dx: {np.std(xf_arr[:, 0])}, Std dy: {np.std(xf_arr[:, 1])}")

    return xf_data, tilt_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute and print alignment statistics for all XF files in a directory.')
    parser.add_argument('xf_dir', type=str, help='Path to directory containing XF files')
    args = parser.parse_args()

    xf_dir = Path(args.xf_dir)
    if not xf_dir.is_dir():
        raise ValueError(f"Provided path {xf_dir} is not a directory.")

    print(f"Computing alignment statistics for all .xf files in directory: {xf_dir}")
    alignment_stats(xf_dir) 
