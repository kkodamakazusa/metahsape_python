![test](https://user-images.githubusercontent.com/74333186/153982668-eebbc20c-86b3-4fa6-b9e6-03ea29afea20.gif)
## Sample dataset
This scrips are checked using Metashape pro v1.7.0.<br>
For ver.2 or later version, script should be edited to run correctly.<br>

### how to use
Put the py and bat files on the same folder with image files.<br>
Then push bat file.<br>
Metashape will perform SfM and output the orthoimage. <br>

Probably, you need to change the metashape path for the bat file.

### Marker conbination
In this dataset, 12bit circular coded marker(printed by metashape) were used.<br>

target ID 121,122,125 and 126 were used<br>
Each distances are...<br>
121-122 = 1.48m<br>
122-126 = 14.4m<br>
125-126 = 1.484m<br>

121&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;125<br>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br>
122 _______126<br>

When you want to use your own configuration, some script should be changed.<br>
make_align.py --> target name<br>
set_drone_coord.py --> target name, region size and box size.<br>

## link for a dataset
https://drive.google.com/file/d/1DGfB4z9Fk9tI_FmqzLYb399E92bQWslB/view?usp=drive_link
