# Smart Document Scanner

**Smart Document Scanner** is software which takes traditional documents as images and recognizes data from it then represents it in a meaningful manner. Traditional way of scanning documents and adding manual data entry is slow and error prone. To reduce man power and faster the process of scanning documents we created **Smart Document Scanner**.

**Smart Document Scanner** takes the document as image crop document from it, identifies type of document, then based type of document retrieves data from it where coordinates of data field are pre-store in JSON file.

## Technology used to build project

### Python dependency

- Flask (micro web framework of connecting user interface with core logic)
- Cv2 (for image processing algorithms)
- Pytesseract (optical character recognition)
- Numpy (manipulate images used along with numpy)
- Json (store property of documents)
- Re (secret labs' regular expression engine)
- Difflib (helpers for computing deltas between objects)
- Os (accessing and creating images and directory)
- Sultan (for using zenity file dialog)
- Peewee (ORM for sqlite)
- Datetime (Accessing date and time)
- Flask_cors (for handling CROS support)

### Frontend

- VueJs 2 (model–view–viewmodel front end JavaScript framework)
- Bulma css (UI kit)
- Axion (Promise based HTTP client for the browser)
- Material Icon (icon pack)

### System

- Zenity (fill selection dialog)
- Sqlite (database)
- Tesseract (OCR)

## Steps to set up the environment and execute project

### Implementation Environment

Python 3 Installation Inside terminal:
`$ sudo apt-get install python3.*`

### Backend Setup

Install following python dependency

flask:
`$ pip install Flask`

cv2:
`$ pip install opencv-python`

pytesseract:
`$ pip install pytesseract`

numpy:
`$ pip install numpy`

sultan:
`$ pip install sultan`

peewee:
`$ pip install peewee`

flask_cors:
`$ pip install flask-cors`

### Tesseract setup

`$ sudo apt-get install tesseract-ocr`

### Adding Gujarati Language Support

`$ sudo apt-get install tesseract-ocr-guj`

### Sqlite setup

`$ sudo apt-get install sqlite3`

### Executing Project

```bash
git clone https://github.com/sameep-baraiya/smart-document-scanner.git
cd smart-document-scanner
export FLASK_APP=login.py
flask run
```

`http://127.0.0.1:5000/` ​ open URL on browser.

## Project Information

### Prepared by

Aghera Manan, Baraiya Sameep

### Under the guidance of

Prof. (Dr.) Vipul Dabhi - Associate Professor & Head, IT Dept., DDU

### Prepared for

System Design Practice - Information Technology - Sem VI Dharmsinh Desai University

## References

[flask](https://flask.palletsprojects.com/en/1.1.x/),
[peewee](http://docs.peewee-orm.com/en/latest/),
[opencv](https://opencv.org/),
[pyimagesearch](http://pyimagesearch.com/),
[flask-cors](https://flask-cors.readthedocs.io/en/latest/),
[sultan](https://sultan.readthedocs.io/en/latest/),
[tesseract](https://github.com/tesseract-ocr/tesseract),
[stackoverflow](https://stackoverflow.com/questions/46731947/detect-angle-and-rotate-an-image-in-python)
