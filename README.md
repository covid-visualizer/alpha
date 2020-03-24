# CoronaCurves -- version0.01

This software attempts to generate visualizations of epidemic and hospital data that leaders can quickly assimilate and use in making effective decisions.

CoronaCurves is easy to set up and run out of the box.  It is not, however, configured to be easily customizable.  If you want different functions you will have to get dirty with the Python code.  Feel free to fork this repository.

Expect evolution in the software and incompatible changes.  CoronaCurves is being made available early -- because that's what an epidemic demands.

* <a href="#requirements">Requirements and installation</a>
* <a href="#features">Features</a>
* <a href="#quirks">Quirks</a>
* <a href="#model">Model and Math</a>
* <a href="#dataconfig">Data Configuration</a>
* <a href="#python">Python code</a>
* <a href="#extensions">Ideas for extensions</a>

Ultimately, getting good data and understanding its baked-in assumptions will be your most difficult task.  That is as it should be.

<a name="requirements"></a>
# Requirements and Installation

You will need Python 2.7 and the following code modules:

* Matplotlib
* Numpy
* Scipy

Use `pip` to install the code modules.  The `requirements.txt` file lists the version numbers that the developer used.  As always, installing inside a virtualenv is recommended.

<a name="quirks"></a>
# Quirks

Geographic regions are universally referred to as "counties."  That is a reflection of the application focus of the original implementation.

<a name="features"></a>
# Features

CoronaCurves produces four classes of graphs, some of which include interesting quantitative data.  In limited areas, it is designed to reflect data uncertainties.  All data are imported from a spreadsheet (.csv) file.

* Plot 0 -- simple graph of cases over time for multiple geographic regions, on a linear axis
    * You can define as many geographic regions you want.  You can use spreadsheet column-summation to define composite geographical areas from smaller ones.
    * Example
    
* Plot 1 -- same as Plot 0, but with a logarithmic y-axis
    * When cases are increasing exponentially, this reduces the exponential curve to a straight line.
    * Use this graph to eyeball whether the epidemic curve is flattening in any geographic region.
    * Example

* Plot 2 -- extrapolated total cases
    * You specify an extrapolation start-date, and CoronaCurves best-fits an exponential to the total-case curve starting at that date.  The best-fit-exponential will appear as a straight line because of the logarithmic y-axis.

* Plot 3 -- danger lines

<a name="model"></a>
# Model and Math

https://stackoverflow.com/questions/3433486/how-to-do-exponential-and-logarithmic-curve-fitting-in-python-i-found-only-poly

<a name="dataconfig"></a>
# Data Configuration

<a name="python"></a>
# Python Code

<a name="extensions"></a>
# Ideas for Extensions

* For each model parameter, make it possible to specify a default value to use in all counties.  This could be done in column 2 of the data spreadsheet or in a YAML file.  Column 2 seems like a better idea -- so everything is visible in one place.
* Add command-line options
    * Set y-axis to logarithmic or linear scale.  Will remove need to have plot 0 and plot 1 as separate entities.
* Clean up all the quirks.
