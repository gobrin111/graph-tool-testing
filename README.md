# graph-tool-testing

This repo provides the test cases that were used to test the overall runtimes and memory usage of each file.

# Installation Instructions

For windows users:<br>
  To use graph-tool on windows, you need to first install Windows Subsystem for Linux(WSL) as described [here](https://learn.microsoft.com/en-us/windows/wsl/install). <br>
  Usually, this requires simply running the command below on the power shell:
```markdown
wsl --install
```
<br>
and then rebooting. You will be asked to provide a username and password.<br>
This will install an Ubuntu subsystem alongside your windows OS. You then can install graph-tool just like described in the Debian/Ubuntu section above, i.e. you should open the file
```markdown
sudo nano /etc/apt/sources.list
```
and add the following line to the bottom:
```markdown
deb https://downloads.skewed.de/apt jammy main
```
