# CoronaCurves -- version0.01

This software attempts to generate visualizations of epidemic and hospital data that leaders can quickly assimilate and use in making effective decisions.

CoronaCurves is easy to set up and run out of the box.  It is not, however, configured to be easily customizable.  If you want different functions you will have to get dirty with the Python code.  Feel free to fork this repository.

Ultimately, getting good data and understanding its baked-in assumptions will be your most difficult task.  That is as it should be.

Expect evolution in the software and incompatible changes.  CoronaCurves is being made available early -- because that's what an epidemic demands.

* <a href="#requirements">Requirements and installation</a>

* <a href="#features">Features</a>

* <a href="#model">Model and Math</a>

* <a href="#dataconfig">Data Configuration</a>

* <a href="#python">Python code</a>

* <a href="#extensions">Ideas for extensions</a>

<a name="requirements"></a>
# Requirements and Installation

You will need Python 2.7 and the following code modules:

* Matplotlib
* Numpy
* Scipy

Use `pip` to install the code modules.  The `requirements.txt` file lists the version numbers that the developer used.  As always, installing inside a virtualenv is recommended.

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

<a name="model"></a>
# Model and Math

https://stackoverflow.com/questions/3433486/how-to-do-exponential-and-logarithmic-curve-fitting-in-python-i-found-only-poly

<a name="dataconfig"></a>
# Data Configuration

<a name="python"></a>
# Python Code

<a name="extensions"></a>
# Ideas for Extensions
