# CoronaCurves -- Version Alpha.1.01

This software attempts to generate visualizations of epidemic and hospital data that leaders can quickly assimilate and use in making effective decisions.

CoronaCurves is easy to set up and run out of the box.  It is not, however, configured to be easily customizable.  If you want different functions you will have to get dirty with the Python code.  Feel free to fork this repository.

Expect evolution in the software and incompatible changes.  CoronaCurves is being made available early -- because that's what an epidemic demands.

* <a href="#requirements">Requirements, installation, and execution</a>
* <a href="#features">Features</a>
* <a href="#quirks">Quirks</a>
* <a href="#model">Model and Math</a>
* <a href="#dataconfig">Data Configuration</a>
* <a href="#python">Python code</a>
* <a href="#extensions">Ideas for extensions</a>

Ultimately, getting good data and understanding its baked-in assumptions will be your most difficult task.  That is as it should be.

<a name="requirements"></a>
# Requirements, Installation, and Execution

You will need Python 2.7 and the following code modules:

* Matplotlib
* Numpy
* Scipy

Use `pip` to install the code modules.  The `requirements.txt` file lists the version numbers that the developer used.  As always, installing inside a virtualenv is recommended.

Execution is normally via the command-line invocation: `python coronacurves.py`

For the moment there are no command-line arguments.  You should execute the above command while your command-line tool has, as its current working directory, the same directory in which `coronacurves.py` is saved.  No fooling with PYTHONPATH is needed.

<a name="quirks"></a>
# Quirks

Geographic regions are universally referred to as "counties."  That is a reflection of the application focus of the original implementation.

Sometimes, if you are graphing several counties in one plot, the title of the plot may get so wide as to chop off the beginning and the end.  If this matters, reduce the number of counties in the plot, or shorten the "short name" for the counties.

The name of the data-input file is hardcoded as `countydata6.csv`.  Sorry about that, but it's easy enough to change in the code.  Ideally, the name should be a command-line argument that has a default.

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

The model fits a line of the form `y = a * exp(b*x)` to a portion of the cases-vs-days curve, where `a` and `b` are the constants that define the best-fit curve.  <a href="https://stackoverflow.com/questions/3433486/how-to-do-exponential-and-logarithmic-curve-fitting-in-python-i-found-only-poly">Stack Overflow</a> shows how to do this.

The doubling time, `d`, in days, is easily calculated as `d = (ln 2)/b`.  The math to prove this is trivially easy.

### Limitations

A simple extrapolation model is valid only in the very near term.  

No sensitivity analysis provided.

<a name="dataconfig"></a>
# Data Configuration

CoronaCurves reads all of its data from a single file: the `countydata6.csv` spreadsheet.  Make sure it is saved in .csv format.

The individual lines of the spreadsheet define one of three things:
* A parameter
    * The full name of the parameter appears in column 1.  The value for each each county appears in its own column in the spreadsheet.
* A numerical value for the number of cases that appeared on that single day
    * The day is specified in column 1 using the `M--D` format.
* A comment
    * If the value of column 1 in the row starts with the string `comment` (upper or lower case) then the line is thereafter ignored.
    
It is not always necessary to include a parameter value for every parameter value.  It depends on the type
of plot being drawn.  Plot 3 requires that all parameters be defined, while Plot 0 requires very few.


### Parameters -- General Remarks

Don't pay attention to the last one or two characters in the name of each parameter.  Those are symbols that tell the software whether the parameter is an integer (#), a floating-point number (##), a character string ($), or a date (^).

### Dates

Dates are specified by the format `M--D` where M and D are the number of the month and the day, respectively.
* Note there are two hyphens between the month number and the day number.  For example the ides of March would be `3--15`
* This unusual format is used because spreadsheets often change the format of entries such as 3/15 into some internal representation for a date that may vary between different spreadsheet vendors.

### Parameters -- Data Dictionary

* `county_name$` = The long name of the county. Is used in plot titles when there is no concern about the length of the title.
* `shortname$` = The short name of the county. Is used in plot titles when there is concern about the length of the title.  Is also used to label lines in the plot.
* `lockdown^` = The date that the county-wide lockdown began, in `M--D` format.
* `staffed_beds#` = The number of hospital beds in the county that have nurses assigned to them.
* `ventilators#` = The number of ventilators in the county.  This is assumed to include ventilators in neonatal ICUs.
* `icu_open_lo##` = The fraction of the county ventilators that determine the lower bound for estimating the number of typically open ICU beds in the county.  That is, the model multiples the number of ventilators in the county by the fractional number `icu_open_lo##` and gets a number of beds that are typically open in that county's ICUs.  This is the minimum number of open beds.
* `icu_open_hi##` = Same as `icu_open_lo##` but is used to calculate the maximum number of ICU beds typically available in the county.

<a name="python"></a>
# Python Code

### Defining new parameters

If you want to add a new parameter to the spreadsheet and to the software, you must pre-define it in the Python code by adding its full name to the other "keys" in `County.legal_keys`

A parameter's "full name" includes one or two terminal characters that specifies the parameter's data-type:
* `#` = integer
* `##` = float
* `$` = string
* `^` = date in `M--D` format

When you use the parameter in Python code, do not use the terminal data-type characters.

New parameters become a value in `County` instances.

### Defining new plots

You're on your own.  The code for this has become a little spaghetti-ish.  Each type of plot is its own class.  At a minimum, it should implement a `draw` method having no arguments except `self`.  

All draw types are called with all county instances.  Your plot class should check if it should draw its plot for each particular county, and if it's not supposed to draw it should just return.

<a name="extensions"></a>
# Ideas for Extensions

* For each model parameter, make it possible to specify a default value to use in all counties.  This could be done in column 2 of the data spreadsheet or in a YAML file.  Column 2 seems like a better idea -- so everything is visible in one place.
* Add command-line options
    * Set y-axis to logarithmic or linear scale.  Will remove need to have plot 0 and plot 1 as separate entities.
* Increase the number of annotations on the curves.  Currently, the only annotation is the county-wide lockdown date.
* Clean up all the quirks.
* Have the software do a sensitivity analysis and produce error bars on the forecast for the number of cases.  Step back day-by-day from the present, dropping that day from the fitting, and tabulate the goodness-of-fit of each fitted curve curve. The error bars could simply be the most deviant curves, above and below the best-fit overall curve.  Note: Can't simply pick the number of days to fit via simple comparison of goodness-of-sit: goodness probably drops monotonically with the number of days included.
