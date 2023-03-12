Photo Namer
===========

The idea of this tool is to get rid of image imports that look like this:

```
test_album/
├── 20230219_0002_01.jpg
├── 20230219_0003.jpg
├── 20230219_0011.jpg
├── 20230219_0022.jpg
├── 20230219_0026.jpg
├── 20230219_0028.jpg
└── 20230219_0029.jpg
```

In favour of semantically meaningful names, but maintaining the order of the files on the album so that they are still readable and make sense as a sequence

```
test_album/
├── 01_this_thing.jpg
├── 02_another_thing.jpg
├── 03_lake.jpg
├── 04_pretty_sunset.jpg
├── 05_mountain.jpg
├── 06_dog.jpg
└── 07_cat.jpg
```

## Developing

The project uses PyQT6, and all the code to run the app is in the file [app.py](app.py). To run the app simply call

```shell
venv/bin/python app.py
```

after all the requirements from the requirements.txt have been installed to a python virtual environment at venv.
