# Vendredi-Noir
Gesture Interface + Multiplay Tetris

## Get Started
```bash
git clone https://github.com/wakame-tech/vendredi-noir.git
cd vendredi-noir
pip install -r requirements.txt
cd src/gui
python main.py
```

> [Note] if occuring server time-out error, check [here](https://vendredi-noir.herokuapp.com) for server activating.

### Skill Stacks
- Python 3.7.3+
- Tensorflow
- Pyautogui
- Flask
- Flask-SocketIO
- PyQt5
- Heroku

### [Memo] Deploy server to Heroku
```
git subtree push --prefix src/server/ heroku master
```

server deployed at [here](https://vendredi-noir.herokuapp.com) 🎉🎉🎉
