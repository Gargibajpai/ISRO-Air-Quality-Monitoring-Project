import requests

link_file = 'subset_M2T1NXSLV_5.12.4_20250707_124333_.txt'

# Read the first .nc4 link from the file
with open(link_file, 'r') as f:
    for line in f:
        url = line.strip()
        if url.endswith('.nc4'):
            nc4_url = url
            break
    else:
        raise ValueError('No .nc4 link found in the file.')

filename = nc4_url.split('/')[-1]

username = input("Earthdata username: ")
password = input("Earthdata password: ")

print(f'Downloading {nc4_url} to {filename}...')

with requests.get(nc4_url, stream=True, auth=(username, password)) as r:
    r.raise_for_status()
    total = int(r.headers.get('content-length', 0))
    with open(filename, 'wb') as f:
        downloaded = 0
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                done = int(50 * downloaded / total) if total else 0
                print(f'\r[{"="*done}{" ".ljust(50-done)}] {downloaded/1e6:.2f}MB/{total/1e6:.2f}MB', end='')
print('\nDownload complete.') 