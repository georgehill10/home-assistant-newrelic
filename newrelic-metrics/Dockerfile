ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-requests

# Copy data
COPY run.sh /
COPY newrelic_sensor.py /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
