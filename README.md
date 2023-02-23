Photo Namer
===========

The idea of this tool is to get rid of image imports that look like this:

```shell
test_album/
├── 20230219_0002_01.jpg
├── 20230219_0003.jpg
├── 20230219_0011.jpg
├── 20230219_0022.jpg
├── 20230219_0026.jpg
├── 20230219_0028.jpg
└── 20230219_0029.jpg
```

In favour of semantically meaningful names, but maintaining the order of the files in the album so that they are still readable and make sense as a sequence

```shell
test_album/
├── 01_this_thing.jpg
├── 02_another_thing.jpg
├── 03_lake.jpg
├── 04_pretty_sunset.jpg
├── 05_mountain.jpg
├── 06_dog.jpg
└── 07_cat.jpg
```