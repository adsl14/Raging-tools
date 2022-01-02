# Raging tools

This tool will help you in order to edit the games Dragon Ball Raging Blast, Dragon Ball Raging Blast 2 and Dragon Ball Z Ultimate Tenkaichi.

It gather all the tools that were made by adsl14, like [vram explorer](https://github.com/adsl14/vram-explorer), [character parameters editor](https://github.com/adsl14/character-parameters-editor) and pak explorer.

Credits to the Raging Blast Modding community and specially to revelation from [XeNTaX](https://forum.xentax.com) forum who made the compress/uncompress tool.

You can get access to the Raging Blast Modding community in the [Discord](https://discord.gg/tBmcwkGUE6) server.

## Requisites

If you want to run the source code, the required packages are the following:

<ul>
  <li>natsort 7.1.1</li>
  <li>numpy 1.21.1</li>
  <li>pyglet 1.5.16</li>
  <li>pyqt5 5.15.4</li>
</ul>

# IMPORTANT!

It is highly recomended to place the tool in <i>Program files</i> because when using <i>pak explorer</i>, 
if the path in Windows is very long, the tool will <b>crash!</b>

Windows has a limit for the path name, so run the tool in a place where the path is not too long 
(<i>Program files</i> for example)

## vram explorer

<img src="images/vram_explorer_main.jpg" alt="vram_explorer_image" width="50%">

<i>vram explorer</i> is a tool that will help you to edit the textures of the game. When you open a <i>.spr</i> and <i>.vram</i> file, the textures will be loaded.

It will show you for each texture, the <b>Resolution</b>, <b>Mipmaps</b> and <b>Encoding</b>. You can export the textures, import over the original, export all the textures, import all the textures from a folder (for this feature, the folder should have the exact filenames of the original textures), remove textures or add a brand new texture. Moreover, you can assign to the material section in the bottom, what texture will be used for that material, and also assign to the 3D model part, what material should use (if there is a 3D model part that doesn't have any material assigned, the game will crash so be aware of removing materials!)

When a texture is imported over a original one, the program will check the new texture file and compare it with the original one. If they have differences in resolution, mipmaps or/and encoding, it will tell you those differences and ask you if you want to import the new texture. However, for images that are originally swizzled, the program won't let you import a texture that has those differences because the swizzle algorithm needs the width and height from the original texture.

## pak explorer

<img src="images/pak_explorer_main.jpg" alt="pak_explorer_image" width="50%">

<i>pak explorer</i> is a tool that will unpack the files that has the extension <i>.zpak</i> (encrypted pak file) or <i>.pak</i> (decrypted pak file). It uses a <i>Depth-first search</i> since the information in those files are stored as a <i>tree graph structure</i>.

When opens a <i>.zpak</i> or <i>.pak</i> file, it will store all the sub-files in disk, in order to write the files propertly. When the algorithm finishes, the tool will show the full path of the sub-files.

You can export the files, import a new one, export all the files or open the folder where those files are located.

## character parameters editor

<i>character parameters editor</i> is a tool that will edit the parameters of the characters, like glow, lightnings, aura size and more. 

Since these files are <i>.zpak</i>, 
the <i>pak explorer</i> will be activated too, and show you all the sub-files that the main <i>.zpak</i> file has.

If you have doubts about what parameter is modifying, leaving the pointer of your mouse in the name of the parameter, it will pop up a description of that parameter.

When saving, it will ask you if the modified values from <i>character parameters editor</i> will be also 
inserted into the unpacked files before repacking everything.

This tool is divided in three tabs:

### general parameters

<img src="images/character_parameters_editor_general_parameters.jpg" alt="character_parameters_editor_general_parameters" width="50%">

This tab holds the general parameters of the characters, like transformations, glow, lightnings, health, aura size, etc.

In order to use this tab, you have open the <i>operate_resident_param.zpak</i> located in <i>st_pack_battle_others_pt_ps3.afs</i>.

### individual parameters

<img src="images/character_parameters_editor_individual_parameters.jpg" alt="character_parameters_editor_individual_parameters" width="50%">

This tab holds the individual parameters of one character. This parameters are the camera values, movement speed, animations, melee values, etc.

In order to use this tab, you have open the <i>operate_character_XYZ_m.zpak</i> (Where XYZ are generic numbers) located in <i>st_pack_battle_character_pt_ps3.afs</i>.

### roster editor

<img src="images/character_parameters_editor_roster_editor.jpg" alt="character_parameters_editor_roster_editor" width="50%">

In this tab you can edit the roster, by adding, removing or swapping characters or transformations.

In order to use this tab, you have open the <i>cs_chip.zpak</i> located in <i>st_pack_progress_pt_ps3.afs</i>.
