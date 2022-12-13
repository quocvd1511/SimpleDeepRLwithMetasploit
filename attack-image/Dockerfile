FROM parrotsec/security
RUN apt -y update && apt -y install python3-pip
RUN pip3 install pymetasploit3 && pip install python3-nmap
RUN mkdir opentools && mkdir sourceDRL
WORKDIR /opentools
RUN git clone https://github.com/t3l3machus/Villain.git && pip3 install -r Villain/requirements.txt
WORKDIR /sourceDRL
RUN git clone https://github.com/quocvd1511/SimpleDeepRLwithMetasploit.git && pip3 install -r SimpleDeepRLwithMetasploit/requirements.txt
