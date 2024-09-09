#!/bin/bash

# Update the system
echo 'Updating the system...'
sudo apt-get update
sudo apt-get upgrade

# Install the necessary packages
echo 'Installing the necessary packages...'
sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev nginx git certbot python3-certbot-nginx mariadb-server mariadb-client

# Install pyenv
echo 'Installing pyenv...'
curl https://pyenv.run | bash
# Configure the .bashrc file
echo 'Configuring the .bashrc file...'
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
exec "$SHELL"

# Install python 3.10
echo 'Installing python 3.10...'
pyenv install 3.10

# Set python 3.10 as the default version
echo 'Setting python 3.10 as the default version...'
pyenv global 3.10

# Clone the repository
echo 'Cloning the repository...'
git clone git@github.com:JDDMR03/UniAmigoModel.git

# Make the virtual environment
echo 'Making the virtual environment...'
cd UniAmigoModel
python -m venv uniamigo

# Install rasa
echo 'Installing rasa...'
source uniamigo/bin/activate
cd model
pip install rasa

# Install mariadb
echo 'Installing mariadb...'
sudo systemctl enable mariadb
sudo mysql_secure_installation

# Configure nginx
echo 'Configuring nginx...'
cat << EOF > /etc/nginx/sites-available/rasa
server {
    server_name model.uniamigomodel.com;  # Replace with your domain or public IP

    # Location block for the Rasa server
    location / {
        proxy_pass http://localhost:5005;  # Rasa server is running on localhost:5005
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS configuration
        add_header "Access-Control-Allow-Origin" "https://uniamigomodel.com" always;
        add_header "Access-Control-Allow-Methods" "GET, POST, OPTIONS, DELETE,PUT" always;
        add_header "Access-Control-Allow-Headers" "Authorization, Origin, X-Requested-With, Content-Type, Accept" always;

        # Handle preflight requests
        if ($request_method = 'OPTIONS') {
            return 204;
        }
    }

    # Location block for the Flask API
    location /api/ {
        proxy_pass http://localhost:5000;  # Flask API is running on localhost:5000
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # CORS configuration
        add_header "Access-Control-Allow-Origin" "https://uniamigomodel.com" always;
        add_header "Access-Control-Allow-Methods" "GET, POST, OPTIONS,DELETE,PUT" always;
        add_header "Access-Control-Allow-Headers" "Authorization, Origin, X-Requested-With, Content-Type, Accept" always;

        # Handle preflight requests
        if ($request_method = 'OPTIONS') {
            return 204;
        }
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/model.uniamigomodel.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/model.uniamigomodel.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}

server {
    if ($host = model.uniamigomodel.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 80;
    server_name model.uniamigomodel.com;
    return 404; # managed by Certbot
}
EOF

# Make enable file
echo 'Making enable file...'
cat << EOF > /home/ubuntu/.local/start_rasa_and_api.sh
#!/bin/bash

# Variables
BASE_DIR="/home/ubuntu/UniAmigoModel"
VENV_DIR="/home/ubuntu/UniAmigoModel/uniamigo"
MODEL_DIR="/home/ubuntu/UniAmigoModel/model"
ACTION_DIR="/home/ubuntu/UniAmigoModel/model/actions"
SCRIPT_PATH="/home/ubuntu/.local/start_rasa_and_api.sh"
SERVICE_FILE="/etc/systemd/system/rasa.service"
USER="ubuntu"
export DB_USER='root'
export DB_PASSWORD=''
export DB_NAME='uniamigo'
export DB_HOST='localhost'
export SECRET_KEY='UniAmigo4Ever'
export MASTER_TOKEN=''

# Start Rasa server
cd /home/ubuntu/UniAmigoModel/model
source /home/ubuntu/UniAmigoModel/uniamigo/bin/activate
rasa run --enable-api --cors "*" &

# Start Rasa actions server
cd /home/ubuntu/UniAmigoModel/model/actions
source /home/ubuntu/UniAmigoModel/uniamigo/bin/activate
rasa run actions &

# Start API
cd /home/ubuntu/UniAmigoModel/api
source /home/ubuntu/UniAmigoModel/uniamigo/bin/activate
python /home/ubuntu/UniAmigoModel/api/main.py
EOF

# Make service file
echo 'Making service file...'
cat << EOF > /etc/systemd/system/rasa.service
[Unit]
Description=Rasa Server and Actions
After=network.target

[Service]
ExecStart=/home/ubuntu/.local/start_rasa_and_api.sh
WorkingDirectory=/home/ubuntu/UniAmigoModel
User=ubuntu
Restart=always
Environment="PATH=/home/ubuntu/UniAmigoModel/uniamigo/bin:/home/ubuntu/.pyenv/shims:/home/ubuntu/.pyenv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"

[Install]
WantedBy=multi-user.target
EOF

# Enable services
echo 'Enabling services...'
sudo systemctl enable rasa
sudo systemctl enable nginx
