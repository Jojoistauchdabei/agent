# Install build dependencies
sudo apt-get update
sudo apt-get install -y python3-dev swig libpulse-dev libasound2-dev

# Clone and build Precise
cd ~
git clone https://github.com/MycroftAI/mycroft-precise.git
cd mycroft-precise
./setup.sh
source .venv/bin/activate
python setup.py install
precise-engine -h  # Test if build was successful

# Create model directory and download model
cd /home/jonas/Schreibtisch/agent
mkdir -p model
wget https://github.com/MycroftAI/precise-data/raw/dist/precise-engine/cortex/precise-engine -O model/precise-engine
chmod +x model/precise-engine
wget https://github.com/MycroftAI/precise-data/raw/models/hey-mycroft.pb -O model/hey-mycroft.pb