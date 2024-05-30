# Define variables
SERVICE_DIR=/etc/systemd/system
BIN_DIR=/usr/bin
SRC_DIR=rpi
SERVICES=$(wildcard $(SRC_DIR)/*.service)
SCRIPTS=$(wildcard $(SRC_DIR)/*.{sh,py})

# Default target
all: rpi-setup

# Combined target to install services and scripts
rpi-setup: install-services install-scripts

# Install service files
install-services: $(SERVICES)
	@echo "Installing service files..."
	@for service in $^; do \
		cp $$service $(SERVICE_DIR)/; \
		echo "Copied $$service to $(SERVICE_DIR)/"; \
	done

# Install and make scripts executable
install-scripts: $(SCRIPTS)
	@echo "Installing and making scripts executable..."
	@for script in $^; do \
		chmod +x $$script; \
		cp $$script $(BIN_DIR)/; \
		echo "Copied $$script to $(BIN_DIR)/ and made it executable"; \
	done

# Clean target (optional, to remove installed services and scripts)
clean:
	@echo "Cleaning installed services and scripts..."
	@for service in $(SERVICES); do \
		rm -f $(SERVICE_DIR)/$$(basename $$service); \
		echo "Removed $(SERVICE_DIR)/$$(basename $$service)"; \
	done
	@for script in $(SCRIPTS); do \
		rm -f $(BIN_DIR)/$$(basename $$script); \
		echo "Removed $(BIN_DIR)/$$(basename $$script)"; \
	done

.PHONY: all rpi-setup install-services install-scripts clean