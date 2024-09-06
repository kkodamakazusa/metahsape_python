![test](https://user-images.githubusercontent.com/74333186/153982668-eebbc20c-86b3-4fa6-b9e6-03ea29afea20.gif)
## Sample dataset
This scrips are checked using Metashape pro v1.7.0.<br>
This script use metashape stand alone module, please see the link of "How to install Metashape stand-alone Python module".<br>
https://agisoft.freshdesk.com/support/solutions/articles/31000148930-how-to-install-metashape-stand-alone-python-module<br>
For ver.2 or later version, script should be edited to run correctly.<br>

### How to use
Put the py and bat files on the same folder with image files.<br>
Then run bat file.<br>
Metashape will perform SfM and output the orthoimage. <br>

Probably, you need to change the metashape path for the bat file.

### Marker conbination
In this dataset, 12bit circular coded marker(printed by metashape) were used.<br>

target ID 121,122,125 and 126 were used.<br>
Each distances are...<br>

121-122 = 1.48m<br>
122-126 = 14.4m<br>
125-126 = 1.484m<br>


From the front view.<br>

121&emsp;&emsp;&emsp;125<br>
|&emsp;&emsp;&emsp;&emsp;&emsp;|<br>
|&emsp;&emsp;&emsp;&emsp;&emsp;|<br>
|&emsp;&emsp;&emsp;&emsp;&emsp;|<br>
122 _______126<br>

When you want to use your own configuration, some script lines should be changed.<br>
make_align.py --> target name<br>
set_drone_coord.py --> target name, region size and box size.<br>

## link for a dataset
[Sample Dataset](https://drive.google.com/file/d/169sAq6X1fRkCL8VzDe0M_otHEqyLFVck/view?usp=drive_link)　(Filesize 18.5GB)<br>
[Sample 3D Point Cloud data (ply)](https://drive.google.com/file/d/1MiwFI7uoc-KvjH0itYHXtmHZj0dzDLd1/view?usp=drive_link) (Filesize 250MB)<br>
![rename_Desktop](https://github.com/user-attachments/assets/ecb89375-9052-4b45-8a9b-06390d2680a2)

