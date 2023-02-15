# kondate

Simple Washoku recipes manager.

## Development

```sh
# Python environment
pip install -r requirements.txt

# Run server (development)
flask --app main --debug run

# Run server
gunicorn 'main:app'
```

### `start.sh` example

```sh
#!/bin/bash

echo Starting Kondate web app.
cd /path/to/app # Edit here
source venv/bin/activate
gunicorn -w 2 -b 127.0.0.1:8080 main:app
```

### `systemd` configure example

```
[Unit]
Description=Kondate Web Application
After=network.target
After=systemd-user-sessions.service
After=network-online.target

[Service]
User=root
Type=simple
ExecStart=/path/to/start.sh
TimeoutSec=30
Restart=on-failure
RestartSec=15
StartLimitInterval=350
StartLimitBurst=10

[Install]
WantedBy=multi-user.target
```

```
sudo cp kondate.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable kondate.service
sudo systemctl start kondate.service
```
