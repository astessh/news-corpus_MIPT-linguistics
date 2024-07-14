import json
import sys
import csv

with open('filtered.json', 'w+', encoding='utf-8') as f:        
    output = []
    for filename in sys.argv[1:]:
        with open(filename) as export_file:
            data = json.load(export_file)
            for message in data['messages']:
                if message['type'] == 'message' and len(message['text_entities']) > 0:
                    parts = [part['text'] for part in message['text_entities']]
                    final_text = "".join(parts)
                    if len(final_text) > 200:
                        output.append({'channel':data['name'], 'id':message['id'], 'text':final_text})
    json.dump(output, f, ensure_ascii=False, indent=4)           
                