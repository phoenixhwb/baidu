FROM python
ADD src/ /baidu/
WORKDIR /baidu/
RUN pip install -r requirement.txt
CMD ["python","main.py"]