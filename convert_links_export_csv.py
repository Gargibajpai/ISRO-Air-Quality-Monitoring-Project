import csv

# Define the base URL
base_url = "https://data.mosdac.gov.in"

# Paste your raw links here as a list
raw_links = [
"https://mosdac.gov.in/download/?r=/download&path=L09yZGVyL0p1bDI1XzEzNTk3My8zUklNR18wMUpVTDIwMjVfMDY0NV9MMkdfQU9EX1YwMlIwMF9BT0QudGlm",
"https://mosdac.gov.in/download/?r=/download&path=L09yZGVyL0p1bDI1XzEzNTk3My8zUklNR18wMUpVTDIwMjVfMDcxNV9MMkdfQU9EX1YwMlIwMF9BT0QudGlm",
"https://mosdac.gov.in/download/?r=/download&path=L09yZGVyL0p1bDI1XzEzNTk3My8zUklNR18wMUpVTDIwMjVfMDc0NV9MMkdfQU9EX1YwMlIwMF9BT0QudGlm",
"https://mosdac.gov.in/download/?r=/download&path=L09yZGVyL0p1bDI1XzEzNTk3My8zUklNR18wMUpVTDIwMjVfMDgxNV9MMkdfQU9EX1YwMlIwMF9BT0QudGlm",
"https://mosdac.gov.in/download/?r=/download&path=L09yZGVyL0p1bDI1XzEzNTk3My8zUklNR18wMUpVTDIwMjVfMDg0NV9MMkdfQU9EX1YwMlIwMF9BT0QudGlm",
"https://mosdac.gov.in/download/?r=/download&path=L09yZGVyL0p1bDI1XzEzNTk3My9pbWFnZXMvM1JJTUdfMDFKVUwyMDI1XzA2NDVfTDJHX0FPRF9WMDJSMDAuanBn",
"https://mosdac.gov.in/download/?r=/download&path=L09yZGVyL0p1bDI1XzEzNTk3My9pbWFnZXMvM1JJTUdfMDFKVUwyMDI1XzA3MTVfTDJHX0FPRF9WMDJSMDAuanBn",
"https://mosdac.gov.in/download/?r=/download&path=L09yZGVyL0p1bDI1XzEzNTk3My9pbWFnZXMvM1JJTUdfMDFKVUwyMDI1XzA3NDVfTDJHX0FPRF9WMDJSMDAuanBn",
"https://mosdac.gov.in/download/?r=/download&path=L09yZGVyL0p1bDI1XzEzNTk3My9pbWFnZXMvM1JJTUdfMDFKVUwyMDI1XzA4MTVfTDJHX0FPRF9WMDJSMDAuanBn",
"https://mosdac.gov.in/download/?r=/download&path=L09yZGVyL0p1bDI1XzEzNTk3My9pbWFnZXMvM1JJTUdfMDFKVUwyMDI1XzA4NDVfTDJHX0FPRF9WMDJSMDAuanBn",   

]

# Create the full URLs
full_urls = [base_url + path for path in raw_links]

# Write to a CSV file
csv_filename = "INSAT3DR_AOD_Links.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["S.No", "Download_URL"])
    for i, url in enumerate(full_urls, start=1):
        writer.writerow([i, url])

print(f"CSV file '{csv_filename}' has been created with {len(full_urls)} URLs.")

