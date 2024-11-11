from util.multipart import parse_multipart
import uuid
import os
from pymongo import MongoClient
from chat import receive_image
from PIL import Image, ImageSequence
import io
import subprocess

client = MongoClient("mongo:27017")
db = client["chat_database"]
chat__collection = db["chat_messages"]


def resize_images(request,handler,filename,part):
    image = Image.open(io.BytesIO(part.content))
    og_width, og_height = image.size
    ratio = og_width/og_height
    print(f"RATIO = {ratio}")

    max_size = 240
    if ratio >= 1:
        print(f"WIDTH > HEIGHT {ratio}")
        final_width = min(og_width, max_size)
        final_height = int(final_width/ratio)
    else:
        print(f"WIDTH < HEIGHT {ratio}")
        final_height = min(og_height, max_size)
        final_width = int(final_height*ratio)
        print(f"INITIAL {(og_width,og_height)} FINAL {(final_width,final_height)}")

    if image.format == "GIF":
        all_frames = []
        for frame in ImageSequence.Iterator(image):
            frame_resized = frame.resize((final_width, final_height))
            all_frames.append(frame_resized)
        output = io.BytesIO()
        all_frames[0].save(output,format="GIF", save_all=True, append_images=all_frames[1:],disposal=2)
    else:    
        image_resize = image.resize((final_width,final_height))
        output = io.BytesIO()
        image_resize.save(output, format=image.format)

    with open(filename, "wb") as file:
        file.write(output.getvalue())
    receive_image(request,handler,filename)

def resize_video(request,handler,filename,part):
    video = io.BytesIO(part.content)
    temp_path = f"public/image/temp_video"
    with open(temp_path, "wb") as temp_video:
        temp_video.write(part.content)

    process = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=s=x:p=0",
            temp_path
        ],
        stdout=subprocess.PIPE,
        text=True
    )

    output = process.stdout.strip()
    og_width = int(output.split("x")[0])
    og_height = int(output.split("x")[1])

    print(f"WIDTH = {og_width}, HIEGHT = {og_height}")

    ratio = og_width/og_height
    print(f"RATIO = {ratio}")

    max_size = 240
    if ratio >= 1:
        print(f"WIDTH > HEIGHT {ratio}")
        final_width = min(og_width, max_size)
        final_height = int(final_width/ratio)
    else:
        print(f"WIDTH < HEIGHT {ratio}")
        final_height = min(og_height, max_size)
        final_width = int(final_height*ratio)
        print(f"INITIAL {(og_width,og_height)} FINAL {(final_width,final_height)}")

    if final_width % 2 != 0:
        final_width -=1
    if final_height % 2 != 0:
        final_height -=1 

    final_size = f"{final_width}X{final_height}"
    print(final_size)

    process = subprocess.run(
        [
            "ffmpeg",
            "-i", temp_path,
            "-s", final_size,
            "-f", "mp4",
            filename
        ],
    )

    os.remove(temp_path)
    receive_image(request,handler,filename)




def upload(request, handler):
    bytes_read = 0
    # print(request.body)
    # print(type(request.body))
    # print(len(request.body))
    ContentLength = int(request.headers["Content-Length"])
    # print(f"len = {ContentLength}")
    while len(request.body) < ContentLength:
        # print("NEED TO BUFFER")
        data = handler.request.recv(2048)
        request.body += data
        print(f"size of body = {len(request.body)}/{ContentLength}")
    obj = parse_multipart(request)
    for i in obj.parts:
        print(i.headers)
        print(i.name)
        if i.name == "upload":
            file_type = None
            if b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01' in i.content:
                file_type = "jpeg"
                print("FOUND JPEG")
            if b'\x89PNG\r\n\x1a\n' in i.content:
                file_type = "png"
                print("FOUND PNG")
            if b'GIF89a' in i.content or b'GIF87a' in i.content:
                file_type = "gif"
                print("FOUND GIF")
            if b'ftypisom' in i.content or b'ftypMSNV' in i.content or b'ftypmp42' in i.content:
                file_type = "mp4"
                print("FOUND MP4")

            filename = f"public/image/image{str(uuid.uuid4())}.{file_type}"
            
            if file_type in ["jpeg","gif","png"]:
                resize_images(request,handler,filename,i)

            if file_type == "mp4":
                resize_video(request,handler,filename,i)