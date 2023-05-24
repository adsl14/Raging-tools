# Raging Tools

Raging Tools is a tool that will help you in order to edit the games from the Raging Blast series. You can edit 
textures, shaders, transformations, parameters, camera values, export/import animations, explore zpak files, etc.

It gathers several tools that were made previously, like [Vram Explorer](https://github.com/adsl14/vram-explorer), 
[Character Parameters Editor](https://github.com/adsl14/character-parameters-editor) and Pak Explorer.

Compatibility list
```
Dragon Ball Raging Blast (PS3 and Xbox 360) -> Only Vram Explorer and Pak Explorer
Dragon Ball Raging Blast 2 (PS3 and Xbox 360)
Dragon Ball Z Ultimate Tenkaichi (PS3 and Xbox 360) -> Only Vram Explorer and Pak Explorer
Dragon Ball Z Zenkai Battle (uncompressed files) -> Only Vram Explorer and Pak Explorer
```

Credits:
<ul> 
  <li>To <b>revelation (revel8n)</b> from <a href=https://forum.xentax.com>XeNTaX</a> forum who made the 
compress/uncompress tool <i>dbrb_compressor.exe</i> and for his contributions.</li>
  <li>To <b><a href=https://github.com/ascomods>Ascomods</a></b>, 
    <b><a href=https://www.youtube.com/c/HiroTenkaichi>HiroTex</a></b>,
    <b><a href=https://www.youtube.com/c/SamuelDBZMAM>SamuelDoesStuff</a></b>, 
    <b>316austin316</b>, <b><a href=https://twitter.com/SSJLVegeta>SSJLVegeta</a></b>, 
    <b><a href=https://www.youtube.com/channel/UC4fHq0fbRMtkcW8ImfQO0Ew>LBFury</a></b>,
    <b><a href=https://www.youtube.com/@KurayamiSaidai/videos>Saidai</a></b> for their contributions.</li>
  <li>To the <a href=https://discord.gg/nShbGxDQsx>Raging Blast Modding community</a>.</li>
</ul>

## Requisites

<ul> 
  <li>If you want to run the <b>source code</b>, the requisites are the following:

Python: ```3.8.13```

Packages:
```
natsort 7.1.1
numpy 1.21.1
pyglet 2.0.5
pyqt5 5.15.4
```
You can install these packages by running: ```pip install -r packages.txt```
  </li>
  <li>A graphic card that is compatible with OpenGL 4.0 or higher is required for <i>Vram Explorer</i>.
  If you're using an <b>Intel Graphic card</b>, make sure the version of the drivers is 21.20.16.4627 or higher, otherwise, <i> Vram Explorer </i> won't show any <i>dds</i> texture. 
  You can update Intel drivers <b><a href=https://www.intel.la/content/www/xl/es/support/detect.html>here</a></b>.</li>
  <li>It is highly recomended to place the tool in <i>Program files</i> because when using <i>Pak Explorer</i>, 
if the path in Windows is very large, the tool will <b>crash!</b>
Windows has a limit for the path name, so run the tool in a place where the path is not too long.</li>
</ul>

## Description

This tool has several options, distributed in tabs. Each of one will be explained in the following sections. 
We will explain first the ones that are on the top of the tool and, after that, the ones that are below.

## File

You can open a file, save it, or close the application. Moreover, for each task, you have a keyboard shortcut.
The type of file you can open or save, will be explained in the following sections.

<img src="images/file_tab.jpg" alt="file_tab_image" width="20%">

## Utilities

Utilities has some individual tasks you can use. The utilities are <i>Compressor</i>, <i>Packer</i> and
<i>Converter</i>

<img src="images/utilities_tab.jpg" alt="file_tab_image" width="20%">

### Compressor

<i>Compressor</i> will use the <i>dbrb_compressor.exe</i> made by <b>revelation (revel8n)</b>. In this option, you can
encrypt or decrypt a single file, or multiple files. The supported files are <i>.zpak</i> <b>(STPZ)</b> and <i>.pak</i>
<b>(STPK)</b> files.
The <i>dbrb_compressor.exe</i> will detect if the input file needs
an encryption or decryption, so there is no need to specify what you need to do.

For the single file option, the tool will generate the output in the same path where the input is located. If is a decryption,
the output file will be <i>.pak</i>. If is a encryption, the output file will be <i>.zpak</i>

For the multiple files option, the tool will ask you the path of the 
folder where the files you want to encrypt or decrypt. The tool will create a folder with the output files, in the same
path where the folder input is located. The name of the output folder will be the same as the input folder, but with the
datetime of creation.

<img src="images/utilities_tab_compressor.jpg" alt="utilities_tab_compressor" width="40%">

### Packer

<i>Packer</i> will unpack the files that are packed as a <i>.pak</i>, or pack a folder with files, creating a output
as a <i>.pak</i> file.

When packing, it will ask you what format do you want to pack the file. 
Select the format depending of the type of files that will be inside the pak file.

Like the previous task, you can unpack or pack, a file or folder respectively, a single one or massivelly.

<img src="images/utilities_tab_packer_unpack.jpg" alt="utilities_tab_packer_unpack" width="40%">
<img src="images/utilities_tab_packer_pack.jpg" alt="utilities_tab_packer_unpack" width="36%">

### Converter

In this tab, you can convert the files to another format. The options are <i>SPA</i> and <i>JSON</i>

You can convert a single <i>SPA</i> to a <JSON> file, or select a folder with some <i>SPA</i> files
and convert all of them, to the <i>JSON</i> format. The same goes if you want to convert from <i>JSON</i>
to <i>SPA</i>

<img src="images/utilities_tab_converter_spa.jpg" alt="utilities_tab_converter_spa" width="40%">
<img src="images/utilities_tab_converter_json.jpg" alt="utilities_tab_converter_json" width="34%">

## Help

In this tab you can check some guides that explains, in a more detail way,
some specifications to take account in order to avoid crashes when running 
the game in real hardware.

<img src="images/help_tab.jpg" alt="help_tab" width="30%">

## About

In this tab you can check the author of the tool, go to the <i>GitHub</i> repository where is explained how to use
the tool, and the people that contribuited in the development of this tool. There is also a link to the <b>Discord</b>
server of the **Raging Blast modding community** where you can join and stay tunned about the news in the modding of
this series.

<img src="images/about_tab.jpg" alt="about_tab" width="30%">

## Vram Explorer

<img src="images/vram_explorer_main.jpg" alt="vram_explorer_image" width="50%">

<i>Vram Explorer</i> is a tool that will help you to edit the textures of the game. When you open a <i>.spr</i> and 
<i>.vram</i> file, the textures will be loaded.

It will show you for each texture, the <b>Resolution</b>, <b>Mipmaps</b> and <b>Encoding</b>. You can export the 
textures, import over the original, export all the textures, import all the textures from a folder (for this feature, 
the folder should have the exact filenames of the original textures), remove textures or add a brand new texture.

When a texture is imported over a original one, the tool will check the new texture file and compare it with the 
original one. If they have differences in resolution, mipmaps or/and encoding, it will tell you those differences and 
you if you want to import the new texture. However, for images that are originally swizzled, the tool won't let you 
import a texture that has those differences because the swizzle algorithm needs the width and height from the original 
texture.

At the bottom of the tool, there is a material section where you can edit the properties of the material. You can 
select the material and change the layers, type, effect, the texture to being used, and the values of the material 
children. In the material children, you can edit the <i>Border color</i> and apply for the transparency value,
the same value to all the materials children by enabling the check <i>Apply 'A' value to all materials</i>. 
Moreover, you can add a new material to the spr, remove the current one, export and import their values 
(and children values if any), export all the values of each material, and import all the values of each material from 
a folder (for this feature, the folder should have the exact filenames of the original materials).

At the bottom of the material section, there is another section where you can assing to a 3D model part, what material 
will be used. <b>WARNING: if there is a 3D model part that doesn't have any material assigned, the game will crash so 
be aware of removing materials!</b>

Lastly, when saving the spr and vram, if this files are from the PS3 version of the game, it will ask you which 
format for the vram output would you like to generate. 
This selection is <b>important</b> since will make the vram more accurate to the game selected, avoiding crashes in 
<b>console</b>.
However, if the spr and vram are from the Xbox 360 version, it won't ask you since this version only needs one single
format.

<b>NOTE</b>: Due to maps spr files has a different structure, <i>Vram Explorer</i> only will let you import or export 
textures. Adding and removing textures, material edition, and assing to a 3D model part a material, won't be allowed 
for now.

## Pak Explorer

<img src="images/pak_explorer_main.jpg" alt="pak_explorer_image" width="50%">

<i>Pak Explorer</i> is a tool that will unpack the files that has the extension <i>.zpak</i> (encrypted pak file) or 
<i>.pak</i> (decrypted pak file). It uses a <i>Depth-first search</i> since the information in those files are stored 
as a <i>tree graph structure</i>.

When opens a <i>.zpak</i> or <i>.pak</i> file, it will store all the sub-files in disk, in order to write the files 
propertly. When the algorithm finishes, the tool will show the full path of the sub-files.

You can export the files, import a new one, export all the files or open the folder where those files are located.

When saving, it will ask you the format of the pak output file. To make it compatible with the console version, select
the proper options according to the pak file you're editing.

## Character Parameters Editor

<i>Character Parameters Editor</i> is a tool that will edit the parameters of the characters, like glow, lightnings, 
aura size and more. 

Since these files are <i>.zpak</i>, 
the <i>Pak Explorer</i> will be activated too, and show you all the sub-files that the main <i>.zpak</i> file has.

If you have doubts about what parameter is modifying, leaving the pointer of your mouse in the name of the parameter, 
it will pop up a description of that parameter.

When saving, it will ask you if the modified values from <i>character parameters editor</i> will be also 
inserted into the unpacked files before repacking everything.

This tool is divided in three tabs:

### General Parameters

This tab holds the general parameters of the characters, like transformations, glow, lightnings, health, aura size, etc.

In order to use this tab, and deppeding on what you need to edit, you have to open one of the following files:
<ul>
  <li>
    <i>operate_resident_param.zpak</i> located in 
<i>st_pack_battle_others_pt_ps3.afs and st_pack_battle_others_pt_x360.afs (Raging Blast 2)</i>.<br>
    <img src="images/character_parameters_editor_general_parameters_1.jpg" 
alt="character_parameters_editor_general_parameters_1" width="50%">
  </li>
  <li>
    <i>db_font_pad_PS3_s.zpak</i> located in <i>st_pack_boot_pt_ps3.afs</i> and
    <i>db_font_pad_X360_s.zpak</i> located in <i>st_pack_boot_pt_x360.afs (Raging Blast 2)</i>.<br>
    <img src="images/character_parameters_editor_general_parameters_2.jpg" 
alt="character_parameters_editor_general_parameters_1" width="50%">
  </li>
</ul>   

### Individual Parameters

<img src="images/character_parameters_editor_individual_parameters.jpg" alt="character_parameters_editor_individual_parameters" width="50%">

This tab holds the individual parameters of one character. This parameters are the camera values, movement speed, 
animations, melee values, signature, etc.

You can change the background color when the character is transforming. However, for some characters this 
option won't be avaliable. To enable it for those characters, you need to export the properties of 'Transformation in' 
in the 'Animation values' from a character that originally has a transformation background, and then import those 
properties to the character you want to change the background color.

The signature can also be swapped too. However, if you're trying to incorporate a signature that triggers a Ki blast,
you need to change the <i>Signature Ki blast</i> values in order to execute the signature propertly.

For the animations, you can export the bones to the <i>.json</i> format and mix the bones in that output file. Then,
you can import the <i>.json</i> file.
Moreover, in the bones section, there is a option called <i>Layer</i>. Since this tool when
opens this kind of files, some <i>spa</i> files are mixed into a custom <i>spas</i> file, that have several <i>spa</i>
data inside, the layer option will let you select, from the _spas_  file, which <i>spa</i> file you want to edit.
Also, for each _rotation_, _translation_ and _unknown_ (this one needs more research. Some <i>spa</i> files has those values),
there is a <i>block</i> section which is related (I think), to the frames of the animation.

In order to use this tab, you have open the <i>operate_character_XYZ_m.zpak</i> (Where XYZ are generic numbers) 
located in <i>st_pack_battle_character_pt_ps3.afs and st_pack_battle_character_pt_x360.afs (Raging Blast 2)</i>.

### Roster Editor

<img src="images/character_parameters_editor_roster_editor.jpg" alt="character_parameters_editor_roster_editor" width="50%">

In this tab you can edit the roster, by adding, removing or swapping characters or transformations.

In order to use this tab, you have open the <i>cs_chip.zpak</i> located in <i>st_pack_progress_pt_ps3.afs and 
st_pack_progress_pt_x360.afs (Raging Blast 2)</i>.
