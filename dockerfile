FROM ubuntu
ADD sources.list /etc/apt/
ADD src/ /baidu/
WORKDIR /baidu/
RUN apt update && apt install -y python3 && apt install -y python3-pip && pip3 install -r requirement.txt
CMD ["python3","main.py"]
