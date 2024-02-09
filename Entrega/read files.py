import os
import urllib.request
from urllib.error import HTTPError, URLError

def remove_empty_lines(data):
    lines = data.split('\n')
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(non_empty_lines)

#Aquesta funcio m'obra els links, provant primer el mes avitual i despres el que alguns cops es fa sevrir
#Ja que alguns messos escampats va canviant( sense un patro aparent)
def open_link_with_condition(year, month, download_dir):
    month = int(month)
    year = int(year)
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_name = month_list[int(month) - 1]
    
    urls = [f'http://www.obsebre.es/php/geomagnetisme/dhorta/{year}/{month_name}/ebr{year}{month:02d}dhor.hor',
            f'http://www.obsebre.es/php/geomagnetisme/dhorta/{year}/{month_name}/ebr20{year}dhor.hor'
           ]

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

    # Create the download directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for url in urls:
        try:
            req = urllib.request.Request(url, headers=hdr)
            response = urllib.request.urlopen(req)

            if response.status == 200:
                data = response.read().decode('utf-8')
                
                data = remove_empty_lines(data)


                # Construct the local file path using os.path.join
                filename = f'ebr{year}{month:02d}dhor.hor'
                full_path = os.path.join(download_dir, filename)

                # Save the data to the specified directory
                with open(full_path, 'w', encoding='utf-8') as local_file:
                    local_file.write(data)

                print(f"Data retrieved successfully and saved to {full_path}")
                return full_path
                break

        except HTTPError as http_err:
            if http_err.code == 404:
                print(f"The link was not found for URL: {url}")
            else:
                print(f"HTTP error occurred for URL: {url}, Error: {http_err}")
        except URLError as url_err:
            print(f"URL error occurred for URL: {url}, Error: {url_err}")

    else:
        print("Failed to retrieve data from all URLs.")

year_initial = int( input('Which initial year do you want to extract data from?'))
year_final = int( input('Which final year do you want to extract data from?'))

for year in range(year_initial, year_final+1):
    for j in range(0,12):
        month = str(j+1).zfill(2)
        file_path = f'C:/Users/pep/OneDrive - UAB/Escritorio/Variacio de D/Dades anys antics/{year}'
        open_link_with_condition(year, month, file_path)