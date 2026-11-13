FROM ubuntu:16.04
RUN apt-get update && apt-get install -y python3 python3-pip gcc libc6-i386 lib32z1
COPY ciscn_2019_c_1 /app/
COPY pwn.c /app/
COPY final_exp.py /app/
WORKDIR /app
RUN chmod +x ./ciscn_2019_c_1
RUN pip3 install pwntools || pip3 install pwntools --break-system-packages 2>/dev/null || true
CMD ["/bin/bash"]
