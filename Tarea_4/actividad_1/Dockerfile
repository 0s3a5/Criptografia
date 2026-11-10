FROM ubuntu:22.04

RUN apt-get update && apt-get install -y openssh-server && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/sshd

RUN useradd -m -s /bin/bash estudiante && \
    echo 'estudiante:cripto2026' | chpasswd

RUN ssh-keygen -A

COPY sshd_config /etc/ssh/sshd_config
RUN chmod 644 /etc/ssh/sshd_config

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]
