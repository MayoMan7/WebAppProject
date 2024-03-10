FROM python:3.8.2
ENV HOME /root
WORKDIR /root
ENV CLIENT_ID="85df4d0b0f974c1b8ba6f2fa9bc80602"
ENV CLIENT_SECRET="574353a0abb84e43b197e328c88b0b7f"
ENV REDIRECT_URI="http://localhost:8080/spotify"
COPY . .
# Download dependancies
RUN pip3 install -r requirements.txt
EXPOSE 8080
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
CMD /wait && python3 -u server.py