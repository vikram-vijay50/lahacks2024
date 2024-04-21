import google.generativeai as genai
import os

GOOGLE_API_KEY = "AIzaSyAJaUSAbrHo_-RH-UuCof9NNvyHcYE40rU"
genai.configure(api_key=GOOGLE_API_KEY)

gemini_responses = {}

Safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

def store_document(file_object, file_name):
    # Check if the target directory exists, if not, create it
    if not os.path.exists("./documents"):
        os.makedirs("./documents")

    # Construct the destination file path
    destination_file_path = os.path.join("./documents", file_name)

    # Write the content of the file object to the destination file
    with open(destination_file_path, 'w') as destination_file:
        destination_file.write(file_object.read())
    
    get_gemini_response(file_name)

def get_documents(directory):
    # List to store the paths of text files
    text_files = []

    # Iterate over each file in the directory
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        # Check if the file is a regular file and has a ".txt" extension
        if os.path.isfile(file_path) and file_name.endswith('.txt'):
            text_files.append(file_path)

    return text_files

def get_document_names(directory):
    # List to store the paths of text files
    text_files_names = []

    # Iterate over each file in the directory
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        # Check if the file is a regular file and has a ".txt" extension
        if os.path.isfile(file_path) and file_name.endswith('.txt'):
            text_files_names.append(file_name)

    return text_files_names

def read_file_to_string(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
    return file_contents

def get_gemini_response(file_name):
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest", safety_settings=Safety_settings)
    doc_path = os.path.join("./documents/", file_name)

    prompt = 'Summarize the important points in the following document. Be detailed, concise, and accurate.' + read_file_to_string(doc_path)
    response = model.generate_content(prompt)
    print(response.text)

def add_to_dict(file_name, response):
    global gemini_responses
    gemini_responses['file_name'] = 'response'