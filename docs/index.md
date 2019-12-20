# Blign Tutorial Video
-- Coming Soon! --

# Introduction
Blign is an alignment and distribution tool for Blender v2.80. It allows users to align and distribute shapes with many different options. Once installed, it can be found in the 3D View Sidebar under the Geometry tab by pressing n. 
<p align="center"><img src="assets/img/Blign.png" /></p>

# Add Object
<p align="center"><img src="assets/img/AddObject.png" /></p>
The Add Object button allows users to select an object and set it as a Blign object. Either one or two objects can be set as a Blign object, and depending on how many are added, different options are available. Once an object has been added the user is given the option to unset it as a Blign object with the Remove Object button. Once an object is added it's name will appear below the Add/Remove Object button.

# Principal Axes
<p align="center"><img src="assets/img/PrincipalAxes.png" /></p>
Blign has three different tabs, each can be used depending on how many objects are added. The Principal Axes tab is to be used when no objects have been added. Within this tab the user has the option to align objects on either the x, y, or z axis. Once the Align button is pressed, all selected object will be moved. The user also has the option to align objects from their centers, or from their most positive or negative x, y, or z points. Depending on which axis is selected, some of these options may not be available. Shown below is an example of the "align to" options available to the user when the x axis is selected.
<p align="center"><img src="assets/img/dropdown.png" /></p>
These points are found using the object's bounding box. Within this tab, the user also has the option to distribute objects, either from their centers or from their edges. By default, Blign will evenly space objects between the first and last object in space. Users also have the option to specify the distance between objects by checking the box next to the spacing button.

# Align to One Object
<p align="center"><img src="assets/img/Alignto1.png" /></p>
This tab is to be used when one object has been added. This tab is has the same options as the Principal Axes tab, except the Align button now aligns objects to where the Blign object is in space. Shown below is an example of 3 different objects being aligned to a cube (highlighted), which has been added as a Blign object. The most negative z (-z) points of each objects are aligned to one another.
<p align="center"><img src="assets/img/alignto1example.png" /></p>

# Align to Two Objects
<p align="center"><img src="assets/img/Alignto2.png" /></p>
This tab is to be used when two objects have been added. When the Align button is clicked, all selected objects will be moved to the closest point on the line between the centers of the 2 Blign objects. Objects can also be aligned outside of the two Blign objects, still along the same line. Users can also distribute objects within this tab. When the Distribute button is clicked, by default Blign will evenly space objects along the same line between the first and last object. Users can also specify the distance between each object by checking the box next to the spacing button. Currently, objects can only be distributed from their centers when two objects have been selected. 
