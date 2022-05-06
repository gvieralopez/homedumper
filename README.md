# homedumper

Computer vision software to automate the process of dumping a Pokemon HOME 
database from a video. 

> This project is still in an early stage and some of the
> instructions below are not yet implemented. 

## 1. Instalation

Make sure you have [Python](https://www.python.org/downloads/) and 
[git](https://git-scm.com/downloads) installed in your system. Then run:

```bash
$ git clone https://github.com/gvieralopez/homedumper.git
$ cd homedumper
$ pip install -r requirements.txt
```

To fetch the source code and install all the dependencies.

## 2. Usage

You can test the program using the sample video provided with this repository:

![](resources/myhome.gif)

### 2.1 Using your own video instead of the default one

If you want to, you can record your own video and place it in the `data` folder. 
Make sure to mimic the one in this repo, paying attention to the following:

1. Place your cursor over `Newest 30` button before start recording.
2. Delete any parts of the video from the begining and the end, that do not contain 
the information of the boxes you want to process

The following step will assume we are using the video from `data/myhome.mp4`,
to apply them to your own video, just use the name of your video instead of
`my_home.mp4`.


### 2.2 Extracting the key frames from your video

The first step of this software is to identify all the independent frames from the video
that capture the status of a HOME box. To do so, simply run:

```bash
$ python -m homedumper extract data/myhome.mp4
```

This will create the following folder structure:

```

    📁output                  
    └── 📁myhome          
        └── 📁frames
            ├── 1.png
            ├── 2.png
            ├── ...
            └── N.png
```

Feel free to delete the images from boxes you don't want to dump to your db (if any).

> ℹ️ Pro tip: If you already have high quality pictures of your HOME boxes (1280 
> x 720), you can create a similar folder structure and proceed with the 
> following step.

### 2.3 Reading the content of each box from the key frames

Once you have the frames you want to process, simply run:

```bash
$ python -m homedumper boxify output/myhome
```

This will read each image and extract the box name from it and as many smaller images
as Pokémon where in that box. After running that command, you will have a folder structure
like this one:

```

    📁output                  
    └── 📁myhome          
        └── 📁frames
        │   ├── 1.png
        │   ├── 2.png
        │   ├── ...
        │   └── N.png
        └── 📁boxes
            ├── 📁HOME 001
            │   ├── 1.png
            │   ├── 2.png
            │   ├── ...
            │   └── 30.png
            ├── 📁HOME 002
            │   ├── 1.png
            │   ├── 2.png
            │   ├── ...
            │   └── 30.png
            ...
```

Note that all folder names inside `boxes` folder correspond to the original boxes names in
the video.


### 2.4 Matching the extracted thumbnails with actual Pokémon data

[Comming soon]
