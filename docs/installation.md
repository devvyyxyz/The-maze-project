# Installation Guide
This guide will help you set up and run the project on your Raspberry Pi 4.

# Prerequisites
1. Raspberry Pi 4 with Raspbian OS installed.
2. Python 3.7+ installed on your Raspberry Pi.
3. Git installed on your Raspberry Pi.

# Step-by-Step Installation
1. Clone the Repository

    Open a terminal and run the following command to clone the repository:
```
git clone https://github.com/yourusername/the-maze-project.git
cd the-maze-project
```

2. Create a Virtual Environment

    It's a good practice to use a virtual environment to manage dependencies. Run the following commands:
```
python3 -m venv venv
source venv/bin/activate
```


3. Install Dependencies

    Install the required Python packages using pip:
```
pip install -r requirements.txt
```

4. Set Up Configuration

    Configure the settings as needed. Open settings.py and modify the configuration parameters according to your setup.

5. Connect Sensors

    Connect the sensors (ultrasonic, infrared, etc.) to the appropriate GPIO pins on your Raspberry Pi. Refer to the sensor documentation for wiring instructions.

6. Run the Application

    Navigate to the `src` directory and run the main application:
```
cd src
python main.py
```

# Additional Information
- Updating the Project
To update the project with the latest changes, navigate to the project directory and pull the latest changes:
```
git pull origin main
```

- Deactivating the Virtual Environment
When you're done working on the project, you can deactivate the virtual environment by running:
```
deactivate
```

# Troubleshooting
- Dependency Issues
If you encounter issues with dependencies, try reinstalling them:
```
pip install --force-reinstall -r requirements.txt
```

- Sensor Connection Issues
Ensure that the sensors are properly connected to the GPIO pins and that the correct pins are specified in the configuration file.


*For further assistance, refer to the documentation or contact the project maintainers.*