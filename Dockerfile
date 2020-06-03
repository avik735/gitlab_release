FROM python:3.7-alpine
COPY release_api.py /bin
RUN pip install python-gitlab
ENTRYPOINT ["/bin/release_api.py"]
CMD ["/bin/bash"]