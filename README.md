# graph-tool-testing

This repo provides the test cases that were used to test the overall runtimes and memory usage of each file.

# For windows users:
  To use graph-tool on windows, you need to first install Windows Subsystem for Linux(WSL) as described [here](https://learn.microsoft.com/en-us/windows/wsl/install). <br>
  Usually, this requires simply running the command below on the power shell:
```markdown
wsl --install
```
and then rebooting. You will be asked to provide a username and password.<br>
This will install an Ubuntu subsystem alongside your windows OS. You then can install graph-tool just like described in the Debian/Ubuntu section above, i.e. you should open the file

```markdown
sudo nano /etc/apt/sources.list
```
and add the following line to the bottom:

```markdown
deb https://downloads.skewed.de/apt jammy main
```
You should then add the signing key:

```markdown
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key 612DEFB798507F25
```
and update the package list:
```markdown
sudo apt-get update
```
To enable all functionalities, the following extra packages need to be installed:
```markdown
sudo apt-get install python3-cairo python3-gi-cairo python3-gi gnome pip
sudo pip install zstandard
```
Finally, the package itself can be installed via:
```markdwon
sudo apt-get install python3-graph-tool
```
Note: This method of installation doesn't work well within virtual machines, since you have to manually add the system packages.
<br>
<br>
<h2>MacOS X installation method</h2><br>
Homebrew<br>
With [Homebrew](https://brew.sh/) the installation is also straightforward, since a [formula](https://formulae.brew.sh/formula/graph-tool) for it is included in the main repository:<br>

```markdown
port install py-graph-tool
```
<br>






