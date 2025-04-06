# Gits v1.0

**Project**: Gits
<br>**Version**: 1.0.2
<br>**OS**: Microsoft / Windows
<br>**Author**: Irakli Gzirishvili
<br>**Mail**: gziraklirex@gmail.com

**Gits** is a Python command-line interface application, designed to help you to work with multiple GitHub and GitLab account repositories on your development machine.

Using **Gits**, you can start cloning from and pushing to multiple GitHub and GitLab accounts without any additional configurations - It automatically sets up everything needed to prevent conflicts between your repositories and accounts.

Disclaimer: Gits CLI app is an independent open-source project (created by Irakli Gzirishvili) and is not affiliated with, endorsed by or officially associated with Git, GitHub or GitLab.

## Installation

To use **Gits**, follow these steps:

- Open CMD and run the following command to install `pip install gits` then restart your CMD
- To check if **Gits** is installed correctly, run the following command `gits`

## Commands

These are the available commands you can use:

- `gits` - To list available commands
- `gits connect` - Setup new ssh connection
- `gits clone (ssh-url)` - Clone project from GitHub / GitLab
- `gits show` - Show existing connections
- `gits drop` - Select connection and drop it

## NOTE

- App will create and edit file 'C:/Users/(username)/.ssh/config' to setup SSH request options.
- App will create SSH key files in folder 'C:/Users/(username)/.gits' to separate them from others (if you have any).
- By default, app will generate and store SSH keys with ssh-keygen rsa 4096 configured command.
