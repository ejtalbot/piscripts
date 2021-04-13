# piscripts

## Install

1. Run `sh noobs_install.sh` script. See [format instructions]
2. Unzip file to the partition `unzip /path/to/noobs.zip /path/to/scdard`
3. Connect pi to power and confirm it is connected to wifi network
4. Run `sudo apt update` and `sudo apt full-upgrade`
5. Git setup with ssh [generate ssh] then [add ssh to github account]
6. `python3 -m venv <env_name>`
7. Install packages with  `pip3 install -r requirements`
8. Need to sudo install th following:
  a. `sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel`
  b. `sudo python3 -m pip install --force-reinstall adafruit-blinka `

[format instructions]: http://qdosmsq.dunbar-it.co.uk/blog/2013/06/noobs-for-raspberry-pi/
[generate ssh]: https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
[add ssh to github account]: https://docs.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account
