import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
import json
from pathlib import Path
import re


def load_json_schema(schema_file):
    """Загружает JSON-схему из файла."""
    try:
        with open(schema_file, 'r', encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Ошибка: Файл схемы {schema_file} не найден.")
        return None  # Важно вернуть None в случае ошибки
    except json.JSONDecodeError:
        print(f"Ошибка: Некорректный JSON в файле {schema_file}.")
        return None



def process_logic(pdf_file):
    schema_file_path = "example.json"
    json_schema = load_json_schema(schema_file_path)

    return extract_invoice_data(pdf_file, json_schema)



def extract_invoice_data(pdf_file, json_schema):
    model = load_model()

    pdf_file_path = Path("") / pdf_file
    if not pdf_file_path.exists():
        print(f"Ошибка: PDF-файл не найден: {pdf_file_path}")
        return

    try:
        sample_pdf = genai.upload_file(pdf_file_path)
    except Exception as e:
        print(f"Ошибка при загрузке PDF: {e}")
        return

    prompt = f"""
            Ты эксперт по распознаванию данных из PDF-инвойсов. Твоя задача - извлечь информацию из предоставленного текста
            и заполнить JSON-структуру согласно предоставленному шаблону.
            В ответе верни **только** корректный JSON, без лишнего текста, 
            не пиши слово json перед ответом, ответ должен начинаться с фигурной скобки
        
            JSON-шаблон:
            ``` {json.dumps(json_schema, indent=4)} ```
        """



    try:
        response = model.generate_content([prompt, sample_pdf])
        if response.text:
            print('------->', response.text)
            cleaned_response = clean_json_response(response.text)
            try:
                extracted_json = json.loads(cleaned_response)
                print("\nИзвлеченный JSON:\n")
                print(json.dumps(extracted_json, indent=4, ensure_ascii=False))
                return extracted_json
            except json.JSONDecodeError:
                print("Ошибка: Gemini вернул некорректный JSON.")
                print("Ответ Gemini:\n", response.text) # Выводим полный ответ Gemini для отладки
        else:
            print("Gemini не вернул никакого текста.")
            return False

    except Exception as e:
        print(f"Ошибка при запросе к Gemini: {e}")
        return False



def write_result_json(data, folder, json_filename):
    json_file_path = os.path.join(folder, json_filename)
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def clean_json_response(response_text):
    """
    Очищает текст JSON, удаляя маркеры формата, лишние символы и экранирование.
    """
    # Убираем префикс и постфикс ```json или ```
    response_text = re.sub(r"```json|```", "", response_text).strip()
    return response_text


def load_model():
    genai.configure(api_key=os.environ.get("API_KEY")) # Используем os.environ.get для обработки отсутствия переменной
    return genai.GenerativeModel("gemini-1.5-flash")