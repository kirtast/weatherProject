FROM alpine:latest

# RUN echo "**** install Python ****" && \
#     apk add --no-cache python3 && \
#     if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
#     \
#     echo "**** install pip ****" && \
#     python3 -m ensurepip && \
#     rm -r /usr/lib/python*/ensurepip && \
#     pip3 install --no-cache --upgrade pip setuptools wheel && \
#     if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi
RUN apk add py3-pip

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /app

COPY . /app

#RUN apk add build-base

RUN pip3 --no-cache-dir install -r requirements.txt
#RUN  python -m pip install -r requirements.txt --no-cache-dir
EXPOSE 5000


ENTRYPOINT ["python3"]

CMD ["API_Flask_app.py"]
