import pathlib
import os
import time

current_dir = pathlib.Path(__file__).parent
all_transcript_path = os.path.join(current_dir, 'all.text')

start = time.time()
for root, dirs, files in os.walk(current_dir):
    # 227 files
    for file_name in files:
        if file_name.endswith('.txt'):
            print(file_name)
            with open(os.path.join(root, file_name), 'r') as file_content:
                transcript = file_content.read()
                with open(all_transcript_path, 'a') as all_transcript:
                    all_transcript.write(transcript + '\n')
        

end = time.time()
print("total time:", (end-start))