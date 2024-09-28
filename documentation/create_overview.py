# dieses script extrahiert aus dem grove wiki, die informationen, 
# ob codecraft unterstützt wird. 

# Verzeichnis mit den Markdown-Dateien
directory = '/home/KingBBQ/src/wiki-documents'



import os
import re
import pandas as pd
import yaml

# Funktion zum Einlesen und Extrahieren der Header-Informationen
def extract_info_from_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # Ersetzen von Tabs durch Leerzeichen im gesamten Dokument
        content = content.replace('\t', '    ')

        # Extrahieren des YAML-Headers
        header_match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
        if header_match:
            header_content = header_match.group(1)
            header_data = yaml.safe_load(header_content)

            # Extrahieren des Titels und des Datums
            title = header_data.get('title', 'No Title')
            date = header_data.get('last_update', {}).get('date', 'No Date')

            # Überprüfen, ob "codecraft" im Dokument vorkommt
            codecraft_present = 'codecraft' in content.lower()

            return title, date, codecraft_present
        else:
            return None, None, False

# Liste zum Speichern der extrahierten Informationen
data = []

# Rekursives Durchlaufen des Verzeichnisses und Verarbeitung der Dateien
for root, dirs, files in os.walk(directory):
    for filename in files:
        if filename.endswith('.md'):
            file_path = os.path.join(root, filename)
            relative_path = os.path.relpath(file_path, directory)
            human_readable_path = os.path.dirname(relative_path).replace('docs/', '')
            title, date, codecraft_present = extract_info_from_markdown(file_path)
            data.append([relative_path, human_readable_path, title, date, codecraft_present])

# Erstellen eines DataFrame und Speichern als CSV
df = pd.DataFrame(data, columns=['Relative Path', 'Human Readable Path', 'Title', 'Date', 'Codecraft Present'])
df = df.sort_values(by='Codecraft Present', ascending=False)

df.to_csv('output.csv', index=False)