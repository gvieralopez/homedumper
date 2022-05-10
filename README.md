[![MIT license](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
![Generations](https://img.shields.io/badge/Generations-1--8-orange)
![Updated for](https://img.shields.io/badge/Updated%20For-Crown%20of%20Tundra-teal)

# homedumper

Computer vision software to automate the dumping process of a Pokemon HOME 
database from a video. Basically, we take a video like this:

![](resources/myhome.gif)

and we give you a `.csv` file with the info:

| Box name  | Slot Number   | Pokémon ID  |
| --------- | ------------- | ----------- |
| Home 001  |      01       |  bulbasaur  |
| Home 001  |      02       |  ivysaur    |
|     ...   |     ...       |    ...      |
| Home 015  |      30       |  zarurde    |


> 🥚 This project is still in an early stage with 
> [many more features and improvements](TODO.md) to come.

## 1. Installation

Make sure you have the following programs installed and added in the `PATH` of 
your system:

* [Python](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads) 
* [Tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html) 

Then, fetch the source code of this project:

```bash
$ git clone https://github.com/gvieralopez/homedumper.git
$ cd homedumper
```

And install software dependencies:

```bash
$ pip install -r requirements.txt
```

## 2. Usage

If you want to test the software with the sample video we provide, just run:

```bash
$ python -m homedumper dump data/myhome.mp4
```

And go grab a cup of ☕ because this could take some minutes.

when the process is finished, you will see a file `match.csv` inside the 
`output` folder. Easy, right?


## 3. What is next?

If you need some help getting the database of your own video or you  want to 
have more control in the different stages of the process, you can see 
[this guide](READMORE.md) with a step-by-step description of what *homedumper*
does.

If you want to know what we are planning to add or improve to this software in
the near future make sure to check [this page](TODO.md).

## 4. Disclaimer

This software comes bundled with data and graphics extracted from the Pokémon 
series of video games. Some terminology from the Pokémon franchise is also 
necessarily used within the software itself. This is all the intellectual 
property of Nintendo, Creatures, inc., and GAME FREAK, inc. and is protected by 
various copyrights and trademarks.

The authors believe that the use of this intellectual property for a fan 
reference is covered by fair use and that the software is significantly 
impaired without said property included. Any use of this copyrighted property 
is at your own legal risk.

This software is not affiliated in any way with Nintendo, Pokémon or any other 
game company.

## 5. Credits

Project developed by [@gvieralopez](https://github.com/gvieralopez/) for educational
purposes.

Thanks to [@itsjavi](https://github.com/itsjavi) for the support with the
assets and the inspiration given by his project [livingdex](https://github.com/itsjavi/livingdex)