# Utilidades

Conjunto de methods, classes, trasnformers, encoders utiles que pueden ser usadas en el futuro.



# Install

Go to `https://github.com/{group}/utilidades` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/utilidades.git
cd utilidades
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
utilidades-run
```
