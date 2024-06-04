# Define variables
SERVICE_DIR=/etc/systemd/system
BIN_DIR=/usr/bin
SRC_DIR=rpi
APP_DIR=app
API_SPEC=openapi.yaml
FLASK_SERVER_DIR=rpi/server
ELECTRON_CLIENT_DIR=app/api

SERVICES=$(wildcard $(SRC_DIR)/*.service)
SCRIPTS=$(wildcard $(SRC_DIR)/*.{sh,py})

# Default target
all: rpi-setup

# Combined target to install services and scripts
rpi-setup: install-rpi-deps install-scripts install-services

# Install deps on rpi
install-rpi-deps:
	@echo "Installing dependencies"
	sudo apt install -y avahi-daemon avahi-discover libnss-mdns
	@echo 'Creating HTTP service definition file'
	sudo sh -c 'echo "<?xml version=\"1.0\" standalone=\'no\'?>\n<!DOCTYPE service-group SYSTEM \"avahi-service.dtd\">\n<service-group>\n  <name replace-wildcards=\"yes\">%h</name>\n  <service>\n    <type>_http._tcp</type>\n    <port>80</port>\n  </service>\n</service-group>" > /etc/avahi/services/http.service'
	@echo "Starting service"
	sudo systemctl start avahi-daemon
	sudo systemctl enable avahi-daemon

# Install service files
install-services: $(SERVICES)
	@echo "Installing service files..."
	@for service in $^; do \
		sudo cp $$service $(SERVICE_DIR)/; \
		echo "Copied $$service to $(SERVICE_DIR)/"; \
	done

# Install and make scripts executable
install-scripts: $(SCRIPTS)
	@echo "Installing and making scripts executable..."
	@for script in $^; do \
		chmod +x $$script; \
		sudo cp $$script $(BIN_DIR)/; \
		echo "Copied $$script to $(BIN_DIR)/ and made it executable"; \
	done

# Generate API stub and client SDK
api:
	@echo "Generating Flask server stub..."
	openapi-generator-cli generate -i $(API_SPEC) -g python-flask -o $(FLASK_SERVER_DIR)
	@echo "Generating JavaScript client SDK..."
	openapi-generator-cli generate -i $(API_SPEC) -g javascript -o $(ELECTRON_CLIENT_DIR)

# Clean target (optional, to remove installed services and scripts)
clean:
	@echo "Cleaning installed services and scripts..."
	@for service in $(SERVICES); do \
		sudo rm -f $(SERVICE_DIR)/$$(basename $$service); \
		echo "Removed $(SERVICE_DIR)/$$(basename $$service)"; \
	done
	@for script in $(SCRIPTS); do \
		sudo rm -f $(BIN_DIR)/$$(basename $$script); \
		echo "Removed $(BIN_DIR)/$$(basename $$script)"; \
	done

.PHONY: all rpi-setup install-services install-scripts api clean
