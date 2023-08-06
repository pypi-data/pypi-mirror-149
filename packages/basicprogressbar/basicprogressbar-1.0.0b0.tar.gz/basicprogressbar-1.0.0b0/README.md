# Basic Progress Bar
Progress bar with no dependencies.

[![Pypi](https://github.com/Sumiza/basicprogressbar/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Sumiza/basicprogressbar/actions/workflows/python-publish.yml)
![PyPI](https://img.shields.io/pypi/v/basicprogressbar)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/basicprogressbar)

<br/>

installation:
```python
from basicprogressbar import BasicProgressBar
```

Arguments:
```python
    current:float = 0       # current progress
    total:float = -1        # total progress '-1' for unlimited
    posttext:str=""         # text behind the bar
    pretext:str="Progress:" # text before the bar
    length:int=60           # length of the bar
    endtext:str=""          # text after the bar when done
    endline:str='\r'        # endline character to rewite same line
```

Basic Examples:

```python
prog = BasicProgressBar(1,10,pretext="Before bar:")
for i in range(11):
    time.sleep(0.1)
    prog.current = i
    prog.endtext = (f"I ended on {i}")
    prog.bar(True)

for i in range(11):
    time.sleep(0.1)
    BasicProgressBar(i,10).bar(True)

prog = BasicProgressBar(1,10)
for i in range(11):
    time.sleep(0.1)
    prog.current = i
    prog.posttext = f"processing {i}"
    print(prog.bar(),end=prog.endline)

prog = BasicProgressBar()
for i in range(10):
    time.sleep(0.1)
    print(prog.next(),end="\r")
print()
```
<br/>

# Discord Progress Bar:
Progress bar for discord
##### Dependencies: requests, time
<br/>

installation:
```python
from basicprogressbar import DiscordProgressBar
```
Arguments:
```python
    # All the arguments of from BasicProgressBar first
    idtoken:str=""              # discord id token
    disuser:str="Progress Bar"  # name of discord user
    throttle:float=0.5          # time between messages
    # shouldnt have to edit the ones below
    messtime:float=0.0          # time used for waiting between messages
    messid:str=""               # message id to edit line
    timeout:float=10.0          # discord timeout
```

Examples:
```python
# all examples from BasicProgressBar apply
token = "23135245523/f43faDSAF-FEAfe24f3qfq-2yfbB-agdagADGA-g334t34gqarGS"

prog = DiscordProgressBar(1,100,idtoken=token)
for i in range(1,101):
    time.sleep(0.1)
    prog.current = i
    prog.send()

prog = DiscordProgressBar(idtoken=token)
for i in range(1,101):
    time.sleep(0.1)
    prog.current = i
    prog.send()

prog = DiscordProgressBar(total=100, idtoken=token)
for i in range(1,101):
    time.sleep(0.1)
    prog.next()
```
