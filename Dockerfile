FROM debian:stretch-slim

RUN echo "python2" > /etc/hostname

RUN apt-get update && apt-get install -y \
	python \
	python-pip \
	python-dev \
	build-essential

RUN apt-get install -y \
	httpie, vim.tiny
RUN pip install httpie-edgegrid

ADD ./assets/akamai /
RUN ln -s /akamai /usr/bin/akamai

CMD ["/bin/bash"]