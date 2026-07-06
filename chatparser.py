from openpyxl import Workbook, load_workbook
import json
import random

with open('result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
messages = data['messages']
random.seed(42)
sample = random.sample(messages, 3000)

def get_text(message):
    text = message.get('text', '')
    if isinstance(text, list):
        return ''.join(part if isinstance(part, str) else part.get('text', '') for part in text)
    return text



wb = Workbook()
sheet = wb.active
sheet.title = "Sample Data"

for i, message in enumerate(sample, start=1):
    message_text = get_text(message)
    print(f"Row {i}: {message_text}")  # Print the message text for debugging
    sheet[f'A{i}'] = message_text

    wb.save("sample_data.xlsx")