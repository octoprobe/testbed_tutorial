# This is how to install Octoprobe and infrastructure_tentacle 

Target OS: Ubuntu 24.04 LTS.

## Installation

Give some permissions

```bash
# Will be used by mpremote and others
sudo usermod -a -G dialout $USER

# TODO: usbhubctl_sysfs

# TODO: picotool

# TODO: dfu-util
```


APT

```bash
sudo apt update \
  && sudo apt upgrade -y \
  && sudo apt install -y git uhubctl dfu-util \
    python-is-python3 python3.12-venv
```

git clone infrastructure_tutorial

```bash
git clone https://github.com/octoprobe/infrastructure_tutorial.git
cd infrastructure_tutorial/
```

python

```bash
python -m venv ~/venv_octoprobe

source ~/venv_octoprobe/bin/activate
pip install --upgrade -r requirements.txt -r requirements-dev.txt
```
