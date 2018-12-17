## Installation 
* create `SimpleImport` directory in `Extensions`, copy `extension.yaml`, `SimpleImport.py`, `romimport.ini` into it.
* or, unpack https://github.com/By6r9/PlayniteScripts/releases/download/0.1/SimpleImport.zip into `Extensions`

## Simple Filename (selected games)
Sets `Name` to the text before first ` (`. Useful if you want to have No-Intro/Redump names. Example:

`Final Fantasy IX (USA) (Disc 1) (v1.1).chd`

**Name:** `Final Fantasy IX`



## Simple Region and Version (selected games)
Sets `Region` with content of the first brackets and `Version` with remaining ones. Example:

`Final Fantasy IX (USA) (Disc 1) (v1.1).chd`

**Region:** `USA`

**Version:** `Disc 1, v1.1`

## Simple Mark Removed
Checks if file in `Image, ROM or ISO Path` field exists on disk. If not, marks it as uninstalled.

**Important notes:**
* script will check all games that are not in `PC` platform. In practice, that means only emulation stuff, but that depends how you organized your library. It shouldn't touch Steam, Uplay, etc. games.
* it won't remove any games
* to check marked games, switch to `Details view`, open filter, select `Uninstalled`, select `Playnite` in `Libraries`.


## Simple Import
Checks for new files in defined directories, then import them with defined emulator profile. 

**Important notes:**
* script tries to import **all** files in defined directory, use it only with clean and sorted collections
* files with TOSEC names (year instead of region in first pair of brackets) are also not supported. They will be , of course, imported but `Region` field will be wrong.
* no support for multi-file iso's (track1.bin, track2.bin, etc.), as above
* added games are logged in `added.log`
* check `playnite.log` for all errors


**Configuration:**

Edit `romimport.ini`. Example:

```
[1]
Platform: Nintendo GameCube
Path: C:\Roms\Nintendo Gamecube\
Emulator: Dolphin
EmulatorProfile: Nintendo GameCube
[2]
Platform: Nintendo Game Boy Advance
Path: C:\Roms\Nintendo Game Boy Advance\
Emulator: RetroArch
EmulatorProfile: mGBA
```
**Important notes:**
* `Platform`, `Emulator` and `EmulatorProfile` fields are case sensitive and must by typed **exactly** as entered in Playnite
* `Path` field is case sensitive and **must** end with `\`
* keep section names (text between `[]`) simple and unique. Used Python library is very picky and expects names like `This Style`.

| Good name  | Bad name  | 
| :------------ |:---------------:| 
| Nintendo Gamecube | Nintendo GameCube |
| Nintendo 3Ds      | Nintendo 3DS |
| Necturbografx 16 | NEC TurboGrafx 16 |
| Microsoft Msx | Microsoft MSX |
| 1 | |
| 2 | |
