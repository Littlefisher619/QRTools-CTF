# QRTools-CTF
Convert a file to QR Code by Python3.
Useful in CTF competitions.
# Installation
```
pip install opencv-python numpy matplotlib
```
# Mode
> * 01 Mode: convert a file including 2 kinds of character
> * xy Mode: convert a file where every line has two numbers means a coordinate point.

# Command
```
qrtools.py <mode: xy | 01> <filename> <size> [ignore]
```
| Argument   | Type      |  Instruction                              |
| :--------: | :-----:   | :---------------------------------------: |
| mode       | String    | Specify **01** or **xy** to choose a mode |
| filename   | String    | File to read                              |
| size       | Integer   | Specify the size of image file            |
| ignore     | String    | Ignore warnings then continue             |

# Example
We provide a hint.txt for you and you can test with it.
```
qrtools.py xy hint.txt 280
qrtools.py xy hint.txt 100 ignore
qrtools.py 01 hint.txt 280
qrtools.py 01 hint.txt 100 ignore
```
