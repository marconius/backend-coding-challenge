FROM python:3.7

ENV SCHEDULER_PROJECT /usr/src/support-shift-scheduler
RUN mkdir $SCHEDULER_PROJECT \
    && chmod -R a+w $SCHEDULER_PROJECT
ENV ORTOOLS_SOLVER_PATH $SCHEDULER_PROJECT/algo-core

# Install balena-io/support-shift-scheduler project and seed input data
RUN url="https://github.com/balena-io/support-shift-scheduler/archive/v1.0.5.tar.gz"; \
    wget "$url" \
    && tar -xvf v1.0.5.tar.gz \
    && pip install -r support-shift-scheduler-1.0.5/requirements.txt \
    && cp -a support-shift-scheduler-1.0.5/* $SCHEDULER_PROJECT \
    && cp support-shift-scheduler-1.0.5/logs-example/support-shift-scheduler-input.json $ORTOOLS_SOLVER_PATH \
    && rm -rf support-shift-scheduler-1.0.5 \
    && rm v1.0.5.tar.gz

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py migrate

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--nothreading"]