import google.generativeai as genai
import cv2
import os
import shutil
from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Model
from typing import List
from pydantic import BaseModel as PydanticBaseModel

# GOOGLE_API_KEY = "AIzaSyAJaUSAbrHo_-RH-UuCof9NNvyHcYE40rU"
# genai.configure(api_key=GOOGLE_API_KEY)

class File:
  def __init__(self, file_path: str, display_name: str = None):
    self.file_path = file_path
    if display_name:
      self.display_name = display_name
    self.timestamp = get_timestamp(file_path)

  def set_file_response(self, response):
    self.response = response

class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class Model(BaseModel):
    x: File = None

class Message(Model):
    message: List[File]

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

RECIPIENT_ADDRESS = "agent1qglnv7fjn6a9r73q27n9967ufckpjq0v3mrtsnu5adsypqesj495kndxx3a"

gen_response_agent = Agent(
    name="gen_response",
    port=8001,
    seed="gen response password",
    endpoint=["http://127.0.0.1:8001/submit"],
)

fund_agent_if_low(gen_response_agent.wallet.address())
print(gen_response_agent.address)

def send_agent_message(agent, content):
    # Construct the message
    message = {
        "sender": gen_response_agent.address,
        "recipient": RECIPIENT_ADDRESS,
        "content": content,
        "type": "Notification"  # Adjust this to your message type
    }

    # Send the message
    agent.send_message(message)

video_file_name = "./uploaded_files/TouretteTics.mp4"
model = None
all_files = []

# Create or cleanup existing extracted image frames directory.
FRAME_EXTRACTION_DIRECTORY = ".\\content\\frames"
FRAME_PREFIX = "_frame"

def create_frame_output_dir(output_dir):
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  else:
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)

def extract_frame_from_video(video_file_path):
  print(f"Extracting {video_file_path} at 1 frame per second. This might take a bit...")
  create_frame_output_dir(FRAME_EXTRACTION_DIRECTORY)
  vidcap = cv2.VideoCapture(video_file_path)
  fps = vidcap.get(cv2.CAP_PROP_FPS)
  frame_duration = 1 / fps  # Time interval between frames (in seconds)
  output_file_prefix = os.path.basename(video_file_path).replace('.', '_')
  frame_count = 0
  count = 0
  while vidcap.isOpened():
      success, frame = vidcap.read()
      if not success: # End of video
          break
      if int(count / fps) == frame_count: # Extract a frame every second
          min = frame_count // 60
          sec = frame_count % 60
          time_string = f"{min:02d}_{sec:02d}"
          image_name = f"{output_file_prefix}{FRAME_PREFIX}{time_string}.jpg"
          output_filename = os.path.join(FRAME_EXTRACTION_DIRECTORY, image_name)
          success = cv2.imwrite(output_filename, frame)
          if success:
            print("Image successfully saved to: ", output_filename)
          else:
            print("Error: Failed to save image to: ", output_filename)
          frame_count += 1
      count += 1
  vidcap.release() # Release the capture object\n",
  print(f"Completed video frame extraction!\n\nExtracted: {frame_count} frames")

def get_timestamp(filename):
  """Extracts the frame count (as an integer) from a filename with the format
     'output_file_prefix_frame00:00.jpg'.
  """
  parts = filename.split(FRAME_PREFIX)
  if len(parts) != 2:
      return None  # Indicates the filename might be incorrectly formatted
  return parts[1].split('.')[0]

# Make GenerateContent request with the structure described above.
def make_request(prompt, files):
  request = [prompt]
  for file in files:
    request.append(file.timestamp)
    request.append(file.response)
  return request

def gen_response():
  extract_frame_from_video(video_file_name)
  # Process each frame in the output directory
  files = os.listdir(FRAME_EXTRACTION_DIRECTORY)
  files = sorted(files)
  files_to_upload = []
  for file in files:
    files_to_upload.append(
        File(file_path=os.path.join(FRAME_EXTRACTION_DIRECTORY, file)))

  # Upload the files to the API
  # Only upload a 10 second slice of files to reduce upload time.
  # Change full_video to True to upload the whole video.
  full_video = False
  file_start = 0
  file_end = 30

  uploaded_files = []
  print(f'Uploading {len(files_to_upload) if full_video else file_end-file_start} files. This might take a bit...')

  for file in files_to_upload if full_video else files_to_upload[file_start:file_end]:
    print(f'Uploading: {file.file_path}...')
    response = genai.upload_file(path=file.file_path)
    file.set_file_response(response)
    uploaded_files.append(file)

  print(f"Completed file uploads!\n\nUploaded: {len(uploaded_files)} files")

  # List files uploaded in the API
  for n, f in zip(range(len(uploaded_files)), genai.list_files()):
    print(f.uri)

  # Create the prompt.
  prompt = """Please describe all changes in behaviors or abnormal behaviors in this video as thoroughly as possible and give the timestamp of when they occurred. 
              Return output in json format: {repeated_behaviors: [{timestamp: timestamp with : replacing _, behavior: repeated behavior, description: description of behavior}]}"""

  # Set the model to Gemini 1.5 Pro.
  model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest", safety_settings=Safety_settings)

  # Make the LLM request.
  request = make_request(prompt, uploaded_files)
  response = model.generate_content(request)
  print(response.text)

  # Write to json file
  print("Writing to JSON file")
  output_json = open('./output_json/output_response.json', 'w')
  output_json.writelines(response.text)
  output_json.close()

  # Call the function to send a message
  gen_response_agent._ctx.send(RECIPIENT_ADDRESS, Message(message=uploaded_files))

  global all_files
  all_files = uploaded_files

def delete_files(uploaded_files):
  print(f'Deleting {len(uploaded_files)} images. This might take a bit...')
  if uploaded_files:
    for file in uploaded_files:
      genai.delete_file(file.response.name)
      print(f'Deleted {file.file_path} at URI {file.response.uri}')
    print(f"Completed deleting files!\n\nDeleted: {len(uploaded_files)} files")

if __name__ == "__main__":
  gen_response_agent.run()