#!/usr/bin/python
import sys
from collections import OrderedDict
try:
	import numpy as np
except:
	print("Unable to import numpy")
	sys.exit()
try:
	from pymatgen.io.vasp.outputs import Vasprun
	from pymatgen.electronic_structure.core import Orbital,Spin,OrbitalType
	from pymatgen.core.periodic_table import Element
except:
	print("Unable to import pymatgen modules")
	sys.exit()
try:
	import matplotlib.pyplot as plt
	import matplotlib.cm as cm
	from matplotlib import rc
except:
	print("Unable to import matplotlib")
	sys.exit()

__author__ = 'saigautam'
__copyright__ = "2021 Indian Institute of Science"
__version__ = "1.4"
__email__ = "saigautamg@iisc.ac.in"
__date__ = "Jul 9, 2021"

#######################################################################################

"""
Code-block below is used for parsing the vasprun.xml.bz2 file and identify if the system is metallic or not

The code-block will not need any change, except in
	possible_els: collection of possible elements that can be present in the system. Change accordingly.
"""

orbitaltypes = {"s":OrbitalType.s, "p":OrbitalType.p, "d":OrbitalType.d, "f":OrbitalType.f}
vr = Vasprun("./vasprun.xml.bz2",parse_eigen=False,parse_projected_eigen=False,parse_potcar_file=False)
structure = vr.structures[0]
possible_els = ["Na","Ca","Mg","Sr","La","Ce","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","O","N","P"]
species = structure.composition.keys()

els = []
for el in possible_els:
	if Element(el) in species:
		els.append(el)

dos = vr.complete_dos
fermi = dos.efermi

try:
	gap,cbm,vbm = dos.get_interpolated_gap(tol=1E-5)
	print("Looks like the structure has a gap of "+str(gap)+" eV. Dotted black lines are band edges.")
	output_string = "Raw data from vasprun (all quantities in eV) \nGap = " \
		+str(gap)+"\nCBM = "+str(cbm)+"\nVBM = "+str(vbm)+"\nFermi = "+str(fermi)+"\n"
	output = open("./gap_data",'w')
	output.write(output_string)
	is_gap_present = True
except:
	print("Looks like structure is metallic. No dotted black lines (VBM/CBM) plotted.")
	output_string = "Raw data from vasprun (all quantities in eV) \nFermi = "+str(fermi)+"\n"
	output = open("./gap_data",'w')
	output.write(output_string)
	is_gap_present = False

#######################################################################################

"""
Code-block here extracts important DOS information that will be plotted eventually.

Important: the if-elif-else block that is defined on orbitaltypes[o] in e_dos.keys() identifies relevant DOS that need plotting
	Only valence DOS of elements are relevant (e.g., p for O, d for Ti---Zn, s for Li, Mg, Ca, Zn, etc.)
	So this if-elif-else block extracts only this relevant information
	Change according to the examples given below
"""
doses = OrderedDict()

for e in els:
	e_dos = dos.get_element_spd_dos(Element(e))
	label = e
	for o in orbitaltypes.keys():
		if orbitaltypes[o] in e_dos.keys():
			if o != "p" and (e == "O" or e == "N" or e == "P"):
				pass
			elif o != "s" and (e == "Ca" or e == "Na" or e == "Mg" or e == "Sr"):
				pass
			elif o == "p" and (e == "Ce" or e == "La" or e == "Cu" or e == "Zn"):
				pass
			elif o == "f" and e != "Ce":
				pass
			elif (o == "p" or o == "s") and (e == "Ti" or e == "V" or e == "Cr" or e == "Mn" or e == "Fe" or e == "Co" or e == "Ni"):
				pass
			else:
				label += "$_"+o+"$"
				e_spd_dos = e_dos[orbitaltypes[o]]
				if is_gap_present:
					energies = e_spd_dos.energies - vbm
				else:
					energies = e_spd_dos.energies - fermi
				densities = e_spd_dos.densities
				doses[label]={'energies':energies, 'densities':densities}
				label = e

#########################################################################################

"""
Matplotlib works in 3 steps:
i) Define all the data that needs to be plotted in x-y arrays (typically numpy arrays)
ii) Plot the data (in terms of lines, contours, bars, etc.)
iii) Define legends, labels, and other text annotations

Matplotlib is also highly flexible in terms of defining plot area, fonts, location of legends, etc.
	But due to this high flexibility, the default settings usually do not yield good figures.
This script is written with generating "publication-ready" figures as an objective.

While lot of plot settings have been optimized, DOS figures are highly system-dependent.
	Hence, changes in some variables may be necessary.
	So, please read the documentation available through this script carefully.
"""
#########################################################################################

"""
Figure setup: don't change this block (i.e., upto the last definition of "rcParams[]").
	This setup should give sans-serif fonts which make for good figures.
		Arial or Helvetica affects the rendering wierdly: not sure why.
	Also sets up latex fonts for rendering super/sub scripts and mathematical formulae.

One variable that can be changed in this block is 
	plt.rcParams['legend.loc']
	If 'upper right' location blocks underlying data, change location of legend box
"""
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.bf'] = 'sans:bold'
plt.rcParams['mathtext.it'] = 'sans:italic'
plt.rcParams['mathtext.rm'] = 'sans'
plt.rcParams['mathtext.default'] = 'rm'
plt.rcParams['mathtext.fallback'] = 'cm'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.usetex'] = True

plt.subplots_adjust(wspace=0)
plt.rcParams['lines.antialiased'] = True

plt.rcParams['legend.fancybox'] = False
plt.rcParams['legend.loc'] = 'upper left'
plt.rcParams['legend.fontsize'] = 'large'
plt.rcParams['legend.framealpha'] = None
plt.rcParams['legend.edgecolor'] = 'black'
plt.rcParams['legend.handlelength'] = 1.5
plt.rcParams['legend.handletextpad'] = 0.5
plt.rcParams['legend.labelspacing'] = 0.5
plt.rcParams['legend.shadow'] = False
plt.rcParams['legend.markerscale']= 0.5

plt.rcParams['xtick.major.size'] = 7
plt.rcParams['xtick.major.width'] = 2.
plt.rcParams['xtick.minor.size'] = 4
plt.rcParams['xtick.minor.width'] = 1.
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['ytick.major.size'] = 7
plt.rcParams['ytick.major.width'] = 2.
plt.rcParams['axes.linewidth'] = 2

#########################################################################################

"""
Define figure area and color schemes after setting up. Things can be changed here.
Variables that can be changed:
    x_plot_lim (defines range of x values that need to be on the plot)
    y_plot_lim (can multiply the relevanty variables with values < 1 to "cut" peaks")
	See further below for y_plot_lim definition and documentation
    x_annotate_offset (to change the position of the label "Fermi" or "VBM" or "CBM" along the x-axis)

ncolors command defines the color scheme used for the plot.
	ncolors will not require change usually, but if too many species present reduce "20" under "round()"

width, height, line_type are generic plotting variables that are used throughout the script

plt.clf() clears the canvas before plotting things.
"""
ncolors = round(20/len(list(doses.keys())))
if ncolors >= 2:
	colors = cm.tab10(np.linspace(0,1,10))
	is_tab10 = True
else:
	print("The color scheme chosen may not be optimal. Reset color scheme if needed")
	ncolors = max(3,len(doses))
	ncolors = min(9, ncolors)
	colors = cm.tab20(np.linspace(0,1,ncolors+1))
	is_tab10 = False

x_plot_lim = [-6,4]

width, height = 18, 8
line_type = "-"   
plt.clf()

#########################################################################################

"""
Code block below, upto the "plt.plot()" function is used to get all data and then plot the individual DOS lines.
This code block will NOT require any changes.
"""
y = None
alldensities = []
allenergies = []
for key,dos in doses.items():
	energies = dos['energies']
	densities = dos['densities']
	
	y = {Spin.up: np.zeros(energies.shape), Spin.down: np.zeros(energies.shape)}
	newdens = {}
	for spin in [Spin.up, Spin.down]:
		newdens[spin] = densities[spin]
	allenergies.append(energies)
	alldensities.append(newdens)

labels = list(doses.keys())
labels.reverse()
alldensities.reverse()
allenergies.reverse()

allpts = []
for i, key in enumerate(labels):
	x = []
	y = []
	for spin in [Spin.up, Spin.down]:
		if spin in alldensities[i]:
			densities = list(int(spin) * alldensities[i][spin])
			energies = list(allenergies[i])
			if spin == Spin.down:
				energies.reverse()
				densities.reverse()
			x.extend(energies)
			y.extend(densities)
	allpts.extend(list(zip(x,y)))

	if is_tab10:
		line, = plt.plot(x,y,linestyle=line_type,linewidth=3,color=colors[i+1])
		line.set_label(str(key))
	else:
		line, = plt.plot(x,y,linestyle=line_type,linewidth=3,color=colors[(i+1) % ncolors])
		line.set_label(str(key))


#########################################################################################

"""
Define range of y values that you would like to appear on the plot.
As of now, the code tries to determine an "optimal" y-range depending on actual values on the DOS-axis.
The variable defining the y-axis range is y_plot_lim: change if needed.
"""
relevanty = [p[1] for p in allpts
        if x_plot_lim[0] < p[0] < x_plot_lim[1]]
y_plot_lim = [-8,8]

#########################################################################################

"""
The if-else code block below plots the Fermi level line, VBM, and CBM, and defines necessary text annotations.
band_edge_color defines the color of the VBM and CBM lines (should be light blue).
axhline() function plots the zero on the DOS axis.
y_annotate_offset and x_annotate_offset define necessary offsets for text labels. Change according to preference.
"""
plt.axhline(y=0.0, linestyle='-', color='black', linewidth=2)
band_edge_color = colors[0]

all_y_range = y_plot_lim[1] - y_plot_lim[0]
y_annotate_offset = 0.1*abs(all_y_range)
x_annotate_offset = 0.1

"""
To get text labels in correct positions on the plot, need to calculate their offset from reference positions.

Note: Although we do calculate offsets, currently we are not actually inserting annotations for non-metallic systems.
In case annotation is needed, uncomment the appropriate lines of code, as indicated by the comments below.

For metallic systems: zero on the energy scale is set to Fermi level, and there will be a dashed black line plotted at energy of 0 (axvline function)
For non-metallic systems: zero on the energy scale is set to VBM, and there will be a dotted blue line plotted
"""
if is_gap_present:
	plt.axvline(x=0.0, linestyle='dotted', color=band_edge_color, linewidth=2)
	plt.axvline(x=cbm-vbm, linestyle='dotted', color=band_edge_color, linewidth=2)
	if abs(vbm-fermi) > abs(cbm-fermi):
		x_fermi_label = -0.5
		x_vbm_label = x_annotate_offset
	else:
		x_fermi_label = x_annotate_offset
		x_vbm_label = -0.5
	"""
	Uncomment following line if Fermi level text annotation is required

	plt.annotate("Fermi", xy = (x_fermi_label,y_plot_lim[0]+y_annotate_offset), size = 18, rotation=90, color='black')


	Uncomment following lines if VBM and CBM text annotations are required

	plt.annotate("VBM", xy = (vbm-fermi+x_vbm_label,y_plot_lim[0]+y_annotate_offset), size = 18, rotation=90, color=band_edge_color)
	plt.annotate("CBM", xy = (cbm-fermi+x_annotate_offset,y_plot_lim[0]+y_annotate_offset), size = 18, rotation=90, color=band_edge_color)
	"""
else:
	plt.axvline(x=0.0,linestyle='dashed',color='black',linewidth=2)
	plt.annotate("Fermi", xy = (x_annotate_offset,y_plot_lim[0]+y_annotate_offset), size = 18, rotation=90, color='black') 

#########################################################################################

"""
Clean up plot. Define axes labels, ticks, and legends
"""
plt.xlabel("Energy (eV)", size=25)
plt.ylabel("Density of states (states/eV)", size=25)

legend = plt.legend(ncol=1)
legend.get_frame().set_linewidth(2)

"""
Other settings, usually won't require changing
"""
plt.tick_params(which="major", bottom=True, top=True, right=True)
plt.tick_params(labelsize=width) 

xtick_range = np.arange(x_plot_lim[0],x_plot_lim[1]+1,1)
str_xticks = []
for j in list(xtick_range):
	str_xticks.append(j)
str_xticks = tuple(str_xticks)
plt.xticks(xtick_range,str_xticks)

"""
Adjust the following line defining ytick_range to display a "few" y-axis values.
	Format is np.arange(min_y_value, max_y_value, y_values_between_ticks). 
	Here 10 means that there is a tick for every 10 y-values. Increase this value if y-axis becomes very crowded.
	The max_y_value is not included while generating ticks. So here, ticks up to 6000, but excluding 6000 are generated.
	va keyword ensures that the y-ticks are correctly aligned with the data displayed.
"""
ytick_range = np.arange(-5000,6000,5)
str_yticks = []
for k in list(ytick_range):
	str_yticks.append(k)
plt.yticks(ytick_range,str_yticks,va='center')


plt.xlim(x_plot_lim)
plt.ylim(y_plot_lim)

#########################################################################################

"""
Save plot. If trying on a local desktop/laptop, plt.show() displays the plot on a GUI before saving on a file.
"""
#plt.show()
plt.savefig("dos.pdf", format="pdf", bbox_inches='tight')
