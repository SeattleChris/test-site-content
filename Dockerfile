FROM gcr.io/google-appengine/python
# LABEL python_version=python
# Create a virtualenv for dependencies. This isolates these packages from system-level packages.
# Use -p python3 or -p python3.7 to select python version. Default is version 2.
RUN virtualenv /env -p python3.7
# Setting these environment variables are the same as running source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
# Install Chrome
# RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
#     && dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install \
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update -qqy \
    && apt-get install -qqy google-chrome-stable \
    && rm /etc/apt/sources.list.d/google-chrome.list \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
# Copy the application's requirements.txt and run pip to install all dependencies into the virtualenv.
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
# CUSTOM run the setup_chrome for Google Chrome and Chromedriver installs.
ADD setup_chrome.py /app/setup_chrome.py
RUN chmod +x /app/setup_chrome.py \
    && /app/setup_chrome.py
# Add the application source code.
ADD . /app
# Run a WSGI server to serve the application. gunicorn must be declared as a dependency in requirements.txt.
CMD gunicorn -b :$PORT main:app