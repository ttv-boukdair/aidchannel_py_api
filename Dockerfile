FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install -y build-essential
RUN apt-get install -y python3.6
RUN apt-get install -y git
RUN apt install -y wget
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN dpkg -i -y google-chrome-stable_current_amd64.deb
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable
RUN apt install -y unzip
# RUN apt-get install -y chromium-chromedriver
# RUN apt-get install -y chromium-browser
RUN wget  http://chromedriver.storage.googleapis.com/92.0.4515.107/chromedriver_linux64.zip
RUN unzip ./chromedriver_linux64.zip
RUN chmod +x ./chromedriver
RUN mv chromedriver /usr/bin


WORKDIR /www
RUN apt install -y python3-pip
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install numpy
RUN python3 -m pip install fastapi
RUN python3 -m pip install uvicorn
RUN python3 -m pip install python-multipart
RUN python3 -m pip install promise
RUN python3 -m pip install requests
RUN python3 -m pip install pandas
RUN python3 -m pip install python-dotenv
RUN python3 -m pip install pymongo
RUN python3 -m pip install twint-fork
# RUN python3 -m pip install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint
RUN python3 -m pip install selenium
RUN python3 -m pip install beautifulsoup4
RUN python3 -m pip install deep-translator
COPY ./src /www/
CMD ["python3","/www/code/index.py"]
