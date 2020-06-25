FROM selenium/standalone-firefox

WORKDIR /home/seluser

RUN sudo apt-get update
RUN sudo apt-get install python3-pip --yes
RUN pip3 install selenium

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
RUN tar -xvf geckodriver-v0.26.0-linux64.tar.gz
RUN sudo chmod +x geckodriver
RUN sudo cp ./geckodriver /usr/bin/

COPY . ./
RUN pip3 install .
