# EyeCatching
This project is to find where your eyes are looking at on a specific picture.

### Use git clone
(1) install all required packages

```angular2html
pip -r install requirements.txt
```

(2) at the same level of *main.py*

```angular2html
python main.py
```

(3) go to your browser for http://127.0.0.1:8000

(4) Upload a picture with its name and points you want to see every time window

(5) After your WebCam is on, look at the picture

(6) You will see your face that indicates collection done, go to http://127.0.0.1:8000/plot

## Use pip install

```angular2html
pip install eyecatching
```

then in iPython
```angular2html
from eyecatching import main
main.main()
```

## Errors
You may see *internal error* when go to the /plot page, that means you do not give the program enough catches, go back to main page, try to decrease the point per plot and try again.

## Tips
You can use different OpenCV, but opencv-python and opencv-contrib-python must have same version.

## Acknowledgements
Inspired and refer to: https://github.com/LukeAllen/optimeyes.git