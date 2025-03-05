# Word Flash
A simple word review application for vocabulary learning.

## Demo
Watch it in action:

![Application Interface](assets/video/demo.png)
![Demo Animation](assets/video/gif_demo.gif)

Full demo video available on [Bilibili](https://www.bilibili.com/video/BV1rB9vYGE8M/)

## Setup
Create a `word_list.txt` file with your vocabulary in this format:
```
word1
definition1
word2
definition2
...
```

## Controls
- `Enter`: Next word
- `L`: Show definition
- `R`: Previous word
- `Q`: Exit review mode
- `C`: Close application
- `G`: Go to some word directly

## How to Run
In advance, you should install the `tqdm` library by running
```bash
pip install tqdm
```
or
```bash
pip3 install tqdm
```
Then


### 1. Direct method:

```bash
python word_start.py
```

or

```bash
python3 word_start.py
```

### 2. For Windows:
 Double click the `Go.bat` file to start the application. Make sure you have adjusted the path in the `Go.bat` file to your python interpreter path.

### 3. For MacOS:
You may want to create a virtual environment if you have more than one python binary files installed.
- Run this command in terminal
  ```bash
   python3 -m venv .venv
   which python3 # should show .venv/bin/python, 
       # otherwise try python/pip instead of python3/pip3
   pip3 install tqdm
  ```
- Then run:
  ```bash
   chmod +x run.command
  ```

- Then simply double click the `run.command` file to start the application.