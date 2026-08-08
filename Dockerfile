FROM kalilinux/kali-rolling:latest

ENV DEBIAN_FRONTEND=noninteractive

# Install ALL pentesting tools + Python
RUN apt-get update && apt-get upgrade -y &&     apt-get install -y --no-install-recommends     nmap sqlmap gobuster nikto hydra wpscan exploitdb whatweb     dirb wordlists seclists     python3 python3-pip python3-dev python3-venv     git curl wget ca-certificates     golang-go unzip     && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install dalfox via Go
RUN go install github.com/hahwul/dalfox/v2@latest &&     cp ~/go/bin/dalfox /usr/local/bin/dalfox ||     (curl -sL https://github.com/hahwul/dalfox/releases/latest/download/dalfox_linux_amd64.tar.gz | tar xz -C /usr/local/bin dalfox)

# Update WPScan database
RUN wpscan --update || echo "WPScan update skipped"

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

COPY . .
RUN mkdir -p /app/checkpoints_real /app/wordlists /app/logs

EXPOSE 5000 8501

CMD ["python3", "use_tool.py", "--api"]
