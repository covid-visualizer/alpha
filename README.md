# CoronaCurves -- Version Alpha.1.01

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

Sometimes, if you are graphing several counties in one plot, the title of the plot may get so wide as to chop off the beginning and the end.  If this matters, reduce the number of counties in the plot, or shorten the "short name" for the counties.

<a name="features"></a>
# Features

CoronaCurves produces four classes of graphs, some of which include interesting quantitative data.  In limited areas, it is designed to reflect data uncertainties.  All data are imported from a spreadsheet (.csv) file. The case numbers are all open source from the <a href="https://projects.sfchronicle.com/2020/coronavirus-map/">San Francisco Chronicle</a> and the hospital capacity numbers are hypothetical.

* Plot 0 -- simple graph of cases over time for multiple geographic regions, on a linear axis
    * You can define as many counties (geographic regions) you want.  You can use spreadsheet column-summation to define composite counties from smaller ones.
    * You can graph multiple counties on one plot.
    * You can annotate each county's line with a mark indicating when the county began lockdown.
    * In all plots, days are counted relative to the day the plot is generated, which is labeled as Day 0.  Negatively-numbered days are in the past. Positively-numbered days are in the future.
    * <a href="https://raw.githubusercontent.com/coronacurves/version01/master/example_plots/plot0_example.png">Example</a>
    
* Plot 1 -- same as Plot 0, but with a logarithmic y-axis
    * When cases are increasing exponentially, this reduces the exponential curve to a straight line.
    * Use this graph to eyeball whether the epidemic curve is flattening in any geographic region.
    * <a href="https://raw.githubusercontent.com/coronacurves/version01/master/example_plots/plot1_example.png">Example</a>

* Plot 2 -- extrapolated total cases
    * You specify an extrapolation start-date, and CoronaCurves best-fits an exponential to the total-case curve starting at that date.  The best-fit-exponential will appear as a straight line because of the logarithmic y-axis.
    * The start of the extrapolation is indicated with a large dot on the plot.
    * The doubling-time for cases is output within the title of the plots.  
    * <a href="https://raw.githubusercontent.com/coronacurves/version01/master/example_plots/plot2_example.png">Example</a>

* Plot 3 -- danger lines
    * This is the most helpful graph for leaders.
    * For a given county, it fuses the expected future growth in cases with the capacity of the healthcare system in that county.
    * Only one county can be shown on a single plot.
    * Currently, these capacities are enabled:
        * Total staffed hospital beds in the county
        * Number of ventilators in the county
        * Estimated number of intensive care unit (ICU) beds that are open on a typical pre-epidemic day.
            * This number is specified as a range
    * The graph shows when the epidemic is expected to hit each of the capacity limits.
        * For the number of ICU beds, the uncertainty in the epidemic is propagated to an uncertainty in the time when that capacity is exceeded.
    * <a href="https://raw.githubusercontent.com/coronacurves/version01/master/example_plots/plot3_example.png">Example</a>

<a name="model"></a>
# Model and Math

A simple extrapolation model is valid only in the very near term.

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
* Increase the number of annotations on the curves.  Currently, the only annotation is the county-wide lockdown date.
* Clean up all the quirks.
