FROM python:3.8
ENV HOME /root
ENV MONGO_URI mongodb://localhost:27017
WORKDIR /root
COPY . .
# RUN apt-get update && apt-get install -y ffmpeg
# Download dependancies
RUN pip3 install -r requirements.txt
EXPOSE 8080
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
CMD /wait && python3 -u server.py
