FROM python:3.7-alpine3.8

LABEL org.label-schema.vendor = "Russell Fenn <rfenn@vt.edu>" \
      org.label-schema.name = "Health Check Playground" \
      org.label-schema.description = "A target for learning about Docker health checks" \
      org.label-schema.schema-version = "1.0"

ENV INSTALL_PATH /hcp
RUN apk --no-cache \
       add curl \
    && pip install \
       bottle \
       gunicorn \
       prometheus_client \
    && rm -rf /root/.cache/pip \
    && rm -rf /lib/apk/db    

COPY hcp.py views $INSTALL_PATH/

WORKDIR $INSTALL_PATH
EXPOSE 10000
CMD ["python", "hcp.py"]
