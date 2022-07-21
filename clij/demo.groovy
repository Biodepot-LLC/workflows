// This script contains a CLIJ2-assistant workflow. You can load this workflow by 
// executing this script in Fijis script editor after choosing the Groovy language.
// 
//                   This script is not meant to be edited.
// 
// For image analysis automation, generate an ImageJ Groovy script for example.
// To make this script run in Fiji, please activate the clij and clij2 update 
// sites in your Fiji. 
// Read more: https://clij.github.io/clij2-assistant/save_and_load

// Generator version: 2.5.1.4

#@ File(style="file", label="Please select an image for the demo...", value="/data/images/000028.raw.tif", persist=false) image_file

import ij.IJ;
import net.haesleinhuepf.clij2.CLIJ2;

println image_file;

// clean up first
IJ.run("Close All");

// Init GPU
clij2 = CLIJ2.getInstance();
clij2.clear();

// disable automatic window positioning 
was_auto_position = net.haesleinhuepf.clij2.assistant.AbstractAssistantGUIPlugin.isAutoPosition();
//net.haesleinhuepf.clij2.assistant.AbstractAssistantGUIPlugin.setAutoPosition(false);

// Load image from disc 
image_1 = net.haesleinhuepf.clij2.assistant.utilities.AssistantUtilities.openImage(image_file.toString());
image_1.setC(1);
image_1.setZ(37);
image_1.setT(1);
image_1.setTitle("000028.raw.tif");
image_1.show();
// copy
node = new net.haesleinhuepf.clij2.assistant.AssistantGUIStartingPoint();
node.setSources(image_1);
node.run("");
node.refreshDialogFromArguments();
node.setTargetInvalid();
// set window position and size
window = node.getTarget().getWindow();
window.setLocation(801, 191);
window.setSize(394, 838);
window.getCanvas().setMagnification(0.75);
image_copy_2 = node.getTarget();
java.lang.Thread.sleep(500);
IJ.run("In [+]");
IJ.run("Out [-]");

// divideByGaussianBackground
node = new net.haesleinhuepf.clij2.assistant.interactive.generic.GenericAssistantGUIPlugin(new net.haesleinhuepf.clij2.plugins.DivideByGaussianBackground());
node.setSources(image_copy_2);
node.run("");
node.getArgs()[2] = 8.0;
node.getArgs()[3] = 8.0;
node.getArgs()[4] = 6.0;
node.refreshDialogFromArguments();
node.setTargetInvalid();
// set window position and size
window = node.getTarget().getWindow();
window.setLocation(833, 156);
window.setSize(394, 838);
window.getCanvas().setMagnification(0.75);
image_divide_by_gaussian_background_3 = node.getTarget();
java.lang.Thread.sleep(500);
IJ.run("In [+]");
IJ.run("Out [-]");

// differenceOfGaussian3D
node = new net.haesleinhuepf.clij2.assistant.interactive.generic.GenericAssistantGUIPlugin(new net.haesleinhuepf.clij2.plugins.DifferenceOfGaussian3D());
node.setSources(image_divide_by_gaussian_background_3);
node.run("");
node.getArgs()[2] = 2.0;
node.getArgs()[3] = 2.0;
node.getArgs()[4] = 2.0;
node.getArgs()[5] = 10.0;
node.getArgs()[6] = 10.0;
node.getArgs()[7] = 10.0;
node.refreshDialogFromArguments();
node.setTargetInvalid();
// set window position and size
window = node.getTarget().getWindow();
window.setLocation(1002, 191);
window.setSize(394, 838);
window.getCanvas().setMagnification(0.75);
image_difference_of_gaussian3d_4 = node.getTarget();
java.lang.Thread.sleep(500);
IJ.run("In [+]");
IJ.run("Out [-]");

// bottomHatBox
node = new net.haesleinhuepf.clij2.assistant.interactive.generic.GenericAssistantGUIPlugin(new net.haesleinhuepf.clij2.plugins.BottomHatBox());
node.setSources(image_difference_of_gaussian3d_4);
node.run("");
node.getArgs()[2] = 2;
node.getArgs()[3] = 2;
node.getArgs()[4] = 2;
node.refreshDialogFromArguments();
node.setTargetInvalid();
// set window position and size
window = node.getTarget().getWindow();
window.setLocation(1091, 212);
window.setSize(394, 838);
window.getCanvas().setMagnification(0.75);
image_bottom_hat_box_5 = node.getTarget();
java.lang.Thread.sleep(500);
IJ.run("In [+]");
IJ.run("Out [-]");

// thresholdOtsu
node = new net.haesleinhuepf.clij2.assistant.interactive.generic.GenericAssistantGUIPlugin(new net.haesleinhuepf.clij2.plugins.ThresholdOtsu());
node.setSources(image_bottom_hat_box_5);
node.run("");
node.refreshDialogFromArguments();
node.setTargetInvalid();
// set window position and size
window = node.getTarget().getWindow();
window.setLocation(1037, 212);
window.setSize(394, 838);
window.getCanvas().setMagnification(0.75);
image_threshold_otsu_6 = node.getTarget();
java.lang.Thread.sleep(500);
IJ.run("In [+]");
IJ.run("Out [-]");

// connectedComponentsLabelingBox
node = new net.haesleinhuepf.clij2.assistant.interactive.generic.GenericAssistantGUIPlugin(new net.haesleinhuepf.clij2.plugins.ConnectedComponentsLabelingBox());
node.setSources(image_threshold_otsu_6);
node.run("");
node.refreshDialogFromArguments();
node.setTargetInvalid();
// set window position and size
window = node.getTarget().getWindow();
window.setLocation(819, 191);
window.setSize(394, 838);
window.getCanvas().setMagnification(0.75);
image_connected_components_labeling_box_7 = node.getTarget();
java.lang.Thread.sleep(500);
IJ.run("In [+]");
IJ.run("Out [-]");

// reset auto-positioning
IJ.wait(500);
net.haesleinhuepf.clij2.assistant.AbstractAssistantGUIPlugin.setAutoPosition(was_auto_position);

