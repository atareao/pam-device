# PAM-DEVICE

![Licencia MIT](https://img.shields.io/badge/Licencia-MIT-green)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b3e704c3f150404582cd23b9fcb4be32)](https://www.codacy.com/manual/atareao/pam-device?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=atareao/pam-device&amp;utm_campaign=Badge_Grade)
[![CodeFactor](https://www.codefactor.io/repository/github/atareao/pam-device/badge/master)](https://www.codefactor.io/repository/github/atareao/pam-device/overview/master)


[![Twitter: atareao](https://img.shields.io/twitter/follow/atareao.svg?style=social)](https://twitter.com/atareao)

PAM DEVICE is a Pluggable Authentication Module for device authentication. You only need to configure a usb device or a bluetooth device, and not password need to access to your laptop or to make `sudo`.


## Prerequisites

Before you begin, ensure you have met the following requirements:

* If you install it from PPA don't worry about, becouse all the requirements are included in the package
* If you clone the repository, you need, at least, these dependecies,

```
libpam-python,
python-pam,
python-bluez,
python3-bluez,
python3,
python3-gi,
gir1.2-gtk-3.0,
gir1.2-gdkpixbuf-2.0
```

## Installing <project_name>

To install **PAM Device**, follow these steps:

* In a terminal (`Ctrl+Alt+T`), run these commands

```
sudo add-apt-repository ppa:atareao/atareao
sudo apt update
sudo apt install pam-device
```

## Using PAM Device

To use **PAM Device**, open PAM Device:


Add run commands and examples you think users will find useful. Provide an options reference for bonus points!

## Contributing to PAM Device

To contribute to **PAM Device**, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contributors

Thanks to the following people who have contributed to this project:

* [@atareao](https://github.com/atareao)

You might want to consider using something like the [All Contributors](https://github.com/all-contributors/all-contributors) specification and its [emoji key](https://allcontributors.org/docs/en/emoji-key).

## Contact

If you want to contact me you can reach me at [atareao.es](https://www.atareao.es).

## License

This project uses the following license: [MIT License](https://choosealicense.com/licenses/mit/).
