# Docker installation
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

# Install git and some needed packages
```bash
sudo apt-get install build-essential python3-dev python3.10-venv software-properties-common git
```

# Manage Docker as Non-Root user
```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

# Docker to start on boot
```bash
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

# Add .env file if needed using Vim
[Vim cheat sheet](https://vim.rtorr.com/)

# Docker build
Navigate to the folder in which you see `Dockerfile`.
```bash
docker build -t amazon-bot .
```

# Docker run
* test run
```bash
docker run amazon-bot
```
* final run
```bash
docker run -d amazon-bot
```