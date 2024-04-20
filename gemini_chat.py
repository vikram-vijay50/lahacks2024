import google.generativeai as genai
import response_gen

exit_key = 'q'

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

RECIPIENT_ADDRESS = "agent1qtvu3wpahhktw0hn55kpr5uvv7erjk5vv0w3ldm2y49n8x4hpfd07tydujm"
all_files = []

FRAME_PREFIX = "_frame"
def get_timestamp(filename):
  """Extracts the frame count (as an integer) from a filename with the format
     'output_file_prefix_frame00:00.jpg'.
  """
  parts = filename.split(FRAME_PREFIX)
  if len(parts) != 2:
      return None  # Indicates the filename might be incorrectly formatted
  return parts[1].split('.')[0]

def initialize_model():
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest", safety_settings=Safety_settings, generation_config=genai.GenerationConfig(
        temperature=0.9,
    ))
    return model.start_chat(history=[])

def send_message_user(model, files, message):
    full_prompt = message + " Be as firm, resolute, and comprehensive as possible in your answer."
    request = response_gen.make_request(message, files)
    response = model.send_message(request)
    return response.text

def get_history(model):
    return model.history

model = initialize_model()
while True:
    # Get user input
    user_input = input("Enter your message (press 'q' to quit): ")

    # Check if the input matches the exit key
    if user_input.lower() == exit_key:
        print("Exiting the loop...")
        break  # Exit the loop if the exit key is pressed

    # Process the user input
    print("Bot: ", send_message_user(model,all_files, user_input))
response_gen.delete_files(all_files)