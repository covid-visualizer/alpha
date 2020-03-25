# -*- coding: utf-8 -*-

"""
CoronaCurves
Version Alpa.1.01
24 March 2020

Draws useful graphs related to an epidemic and its intersection with hospital capacities.

This software is in the public domain.
"""

"""
A few programming notes:
* The format for a date-specifier is determined by < utils.is_date_spec >, e.g. 3--15
"""

import csv
import time
import math
import subprocess
import datetime

import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.optimize

import utils

class DayCase:    
    def __init__( self, month, day, val_string ):
        self.month = month
        self.day = day
        self.val = int( val_string )
        self.day_of_year = utils.day_of_year( self.month, self.day )
        self.offset = self.day_of_year - utils.BASE_DAY_DAYOFYEAR       
    
class CasesList:
    def __init__( self ):
        self.day_values = []
        self.ndays = None                  # set in < tidy_case_list > method

    def add1day( self, val_string, month, day ):
        self.day_values.append( DayCase( month, day, val_string ) )
    
    def tidy_case_list( self ):
        self.ensure_no_duplicates()
        self.ndays = len(self.day_values)
    
    def iivv( self, day_values=None ):
        day_values = day_values or self.day_values
        day_values.sort( key=lambda obj: obj.offset )
        ii = [ daycase.offset for daycase in day_values ]
        vv = [ daycase.val    for daycase in day_values ]
        return ii, vv

    def ensure_no_duplicates( self ):
        uniques = set( [ daycase.day_of_year for daycase in self.day_values ] )
        assert len(uniques)==len(self.day_values), 'Duplicate day-data somewhere in sheet'
   
    def project( self, n_days ):
        ii_ofdata = np.array([ daycase.offset for daycase in self.day_values ])
        vv_linear = np.array([ daycase.val    for daycase in self.day_values ])
        vv_logged = np.log( vv_linear )
        p_opt, p_cov = scipy.optimize.curve_fit(lambda t,a,b: a*np.exp(b*t), ii_ofdata, vv_linear,  p0=None)
        #print 793333, p_opt
        #print 794444, p_cov
        ii_predict = sorted( set( list(ii_ofdata) + range(n_days+1) ) )
        ii_predict = np.array( sorted(ii_predict) )
        vv_fit = p_opt[0]*np.exp(p_opt[1]*ii_predict)
        return list(ii_predict), list(vv_fit), p_opt

class CasesListBatch( CasesList ):
    def __init__( self, day_values ):
        self.day_values = day_values
        self.ndays = len( self.day_values )

class Datum:

    @classmethod
    def Instantiate( cls, rownum, colnum, key, val_string ):
        if key.endswith('##'):  return FloatDatum(   rownum, colnum, key, key[:-2], val_string )
        elif key.endswith('#'): return IntegerDatum( rownum, colnum, key, key[:-1], val_string )
        elif key.endswith('^'): return DaypairDatum( rownum, colnum, key, key[:-1], val_string )
        else:                   return StringDatum(  rownum, colnum, key, key,      val_string )

    def __init__( self, rownum, colnum, keyname, nicename, val_string ):
        self.var_name = nicename
        self.key_name = keyname
        try:
            fn = self.val_converter
            #print 3313, fn, val_string
            self.value = apply( fn, (val_string,) )
        except:
            raise Exception( 'Error in row %d / col %d: Expected %s, which %s is not.' %
                             ( rownum, colnum, self.val_typename, val_string ) )

    #def __repr__( self ):
    #    return '<%s.%s>' % (self.__class__.__name__, self.key_name )

class DaypairDatum( Datum ):
    val_converter = lambda x, y: utils.is_date_spec(y)
    val_typename = 'a date'

class FloatDatum( Datum ):
    val_converter = float
    val_typename = 'a number'

class IntegerDatum( Datum ):
    val_converter = int
    val_typename = 'an integer'

class StringDatum( Datum ):
    val_converter = str
    val_typename = 'a string'



class County:
    legal_keys = filter( None, [ x.strip() for x in """county_name
                                                       shortname
                                                       icu_total#
                                                       icu_open#
                                                       icu_fraction##
                                                       hosp_fraction##
                                                       staffed_beds#
                                                       ventilators#
                                                       icu_open_hi##
                                                       icu_open_lo##
                                                       lockdown^
                                                       project_from^
                                                       project_ndays#
                                                       drawplot0#
                                                       drawplot1#
                                                       drawplot2#
                                                       drawplot3#
                                                       """.split('\n') ] )
    
    def __init__( self ):
        self.cases_list = CasesList()
    
    def __repr__( self ):
        return "<%s.%s>" % ( self.__class__.__name__, self.county_name )

    def add1( self, is_date_row, rownum, colnum, key, val_string ):
        if is_date_row:
            self.cases_list.add1day( val_string, *is_date_row )
        else:
            value_instance = Datum.Instantiate( rownum, colnum, key, val_string )
            assert value_instance.key_name in self.legal_keys, \
                   'In row %d got unexpected variable name: %s' % ( rownum, key )
            assert value_instance.key_name not in self.__dict__.keys(), \
                   'In row %d found duplicate variable name: %s' % ( rownum, key )
            setattr( self, value_instance.var_name, value_instance.value )

    def tidy( self ):
        self.cases_list.tidy_case_list()

class Plot:
    yscale = 'log'

    def __init__( self, counties ):
        my_var = 'drawplot%s' % self.__class__.__name__[-1]
        self.my_counties = [ c for c in counties if getattr( c, my_var ) ]
        #self.axes_layout = self.calculate_n_axes( self.my_counties )
        self.init2()
    
    def init2( self ): pass
    
    def calculate_n_axes( self, _ ):
        fig, ax = plt.subplots()
        return fig, [ax,]
        
    def draw( self ):
        plt.figure()
        fig, axlist = self.calculate_n_axes( self.my_counties )
        if self.my_counties:
            print 'Starting %s for counties %s' % ( self.__class__.__name__, self.my_counties )
            self.draw_each_county( axlist )
            self.draw_standard( axlist )
            fig_title = self.calc_title( self.my_counties )
            if fig_title: plt.title( fig_title )
            pathname = self.save()
            print '    Wrote to %s' % pathname
    
    def draw_each_county( self, axlist ):
        ax_i = 0
        ax_increment = 1 if axlist[1:] else 0
        for county in self.my_counties:
            ax = axlist[ ax_i ]
            ii,vv = county.cases_list.iivv()
            ax.plot( ii, vv )
            ax.text( ii[-1], vv[-1], ' '+county.shortname, 
                horizontalalignment='left', verticalalignment='center' )
            if getattr( county, 'lockdown', None ):
                month, day = county.lockdown
                dc = DayCase( month, day, '0' )
                i = ii.index( dc.offset )
                #hline( ax, dc.offset, dc.offset+6, vv[i], '+' )
                #hline( ax, dc.offset, dc.offset+6, vv[i] )
                ax.plot( [dc.offset,], [vv[i],], '+' )
            self.xmin = ii[0]
            self.xmax = ii[-1]
            xx, yy, p_opt = self.draw_extrapolation( county, ax ) # sets doubling_time and extrapolation_offset
            self.draw_dangerlines( county, ax, xx, yy, p_opt )
            ax_i += ax_increment

    def draw_extrapolation( self, *_ ): return 0,0,0

    def draw_dangerlines( self, *_ ): pass

    def draw_standard( self, axlist ):
        from matplotlib.ticker import MaxNLocator
        for ax in axlist:
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.minorticks_on()
            ax.tick_params(axis='y',which='minor',bottom=False)
            ax.set_yscale( self.yscale )
            today = 'Days relative to %s' % utils.BASE_DAY_STRING
            ax.set_xlabel(today )
            ax.set_ylabel('Number of Cases')

    def save( self ):
        pathname = '%s_%s.png' % ( self.__class__.__name__.lower(), int(time.time()) )
        plt.savefig( pathname )
        subprocess.call([ "open", pathname ])
        return pathname

class Plot0( Plot ):
    yscale = 'linear'
    
    def calc_title( self, my_counties ):
        county_str = ' -- '.join( [ c.county_name for c in my_counties ] )
        return 'Cumulative Cases of COVID-19\n' + county_str        

class Plot1( Plot0 ): yscale = 'log'

class Plot2( Plot ):
    yscale = 'log'
   
    def calc_title( self, my_counties ):
        line1 = r"Extrapolated Cases of COVID-19: Epochs and Doubling-Times (d$^2$)"
        parts = [ r"%s/%s/%.1fd$^{2}$" % ( c.shortname, utils.offset_string(c.extrapolation_offset), c.doubling_time ) 
                  for c in my_counties ]
        line2 = r" $\bullet$ ".join( parts )
        #line2 = r"%s $\Longleftrightarrow$ %.1f-day doubling time" % ( county_str, self.doubling_time )
        return line1 + '\n' + line2
    
    def draw_extrapolation( self, county, ax ):
        daypair = county.project_from
        day_of_year = utils.day_of_year( *daypair )
        day_values = [ dv for dv in county.cases_list.day_values 
                       if dv.day_of_year>=day_of_year ]
        c = CasesListBatch( day_values )
        xx, yy, p_opt = c.project( county.project_ndays )
        ax.plot( xx, yy, '--k', linewidth=0.4 )
        ax.plot( xx[:1], yy[:1], 'o' )
        ax.text( xx[-1], yy[-1], ' Cases' )
        self.xmin = min( self.xmin, xx[0] )
        self.xmax = max( self.xmax, xx[-1] )
        county.extrapolation_offset = day_values[0].offset
        county.doubling_time = math.log(2) / p_opt[1]
        return xx, yy, p_opt

class Point:
    def __init__( self, x, y ):
        self.x = x
        self.y = y

class Plot3( Plot2 ):
    yscale = 'log'
    subplot_wd_inches = 8
    subplot_ht_inches = 7
    
    def calculate_n_axes( self, my_counties ): 
        n = len(my_counties)
        if n<=1:
            fig, ax = plt.subplots()
            axlist = [ax,]
            hw = (1,1)
        elif n==2:
            fig, (ax1,ax2) = plt.subplots(1,2)
            axlist = [ax1,ax2]
            hw = (1,2)
        elif n<=4:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
            axlist = [ax1,ax2,ax3,ax4]
            hw = (2,2)
        fig.set_size_inches( hw[1]*self.subplot_wd_inches, hw[0]*self.subplot_ht_inches )
        return fig, axlist

    def calc_title( *_ ): return ''

    def draw_dangerlines( self, county, ax, xx, yy, p_opt ):
        # < xx > and < yy > are the points plotted for the county total-cases.
        line_color = 'xkcd:light grey'
        def intersect( fraction, y, label ):
            ax.text( self.xmin, y, label, verticalalignment='bottom' )
            x = math.log( y/(fraction*p_opt[0]) ) / p_opt[1]
            vline( ax, x, 0, y, line_color )
            hline( ax, self.xmin, x, y, line_color )
            ax.plot( [x,], [y,], 'ok' )
            return Point(x,y)
        def fracline( yy, label ):
            ax.plot( xx, yy, ':' )
            ax.text( xx[-1], yy[-1], label )
        fracline( [ county.icu_fraction*y  for y in yy ], '  ICU pts' )
        fracline( [ county.hosp_fraction*y for y in yy ], 'Hosp. pts' )
        xy0 = intersect( county.icu_fraction,  county.ventilators, 'Ventilators' )
        xy1 = intersect( county.icu_fraction,  county.icu_open_hi * county.ventilators , '' )
        xy2 = intersect( county.icu_fraction,  county.icu_open_lo * county.ventilators , 
              'Est. open ICU beds =\n%d%%-%d%% of "Ventilators"' %
              (100*county.icu_open_lo, 100*county.icu_open_hi) )
        yBot = 1
        xMin = self.xmin
        points = [ (xMin, xy1.y), (xy1.x, xy1.y), (xy1.x, yBot), (xy2.x, yBot), (xy2.x, xy2.y), (xMin, xy2.y), (xMin, xy1.y) ]
        ax.fill( [ x for x,y in points ], [y for x,y in points], line_color )
        #x1 = intersect( county.icu_fraction,  county.icu_total, 'Total ICU beds' )
        #x2 = intersect( county.icu_fraction,  county.icu_open, 'Typical ICU\nbeds open' )
        xy3 = intersect( county.hosp_fraction, county.staffed_beds, 'Staffed hosp-beds' )
        if 0 and self.yscale == 'log':
            def color( y, name ):
                plt.text( xx[-1], y, ' ' + name, fontdict={'size':6,}, verticalalignment='center' )
                hline( ax, x2, xx[-1], y, ':' )
            color( county.icu_open, 'AMBER' )
            color( 1.5*county.icu_open, 'RED = 1.5x' )
            color( 2*county.icu_open, 'BLACK = 2x' )
        ax.set_title( county.county_name + '\n' + r"%s extrapolation $\bullet$ %.1f days to double" % (
                utils.offset_string(county.extrapolation_offset), county.doubling_time ) )

def hline( ax, x1, x2, y, *args, **kwargs ): ax.plot( [x1,x2], [y,y], *args, **kwargs )
def vline( ax, x, y1, y2, *args, **kwargs ): ax.plot( [x,x], [y1,y2], *args, **kwargs )
    
def main():
    with open( 'countydata6.csv', 'rU' ) as f:
        csv_reader = csv.reader( f )
        row_number = 0
        for row in csv_reader:
            column_vals = list( row )
            row_number += 1
            if row_number==1:
                counties = [ County() for column in column_vals[1:] ]
                column_numbers = [ i+2 for i,_ in enumerate( counties ) ]
            varname = column_vals[0].strip()
            if not varname.lower().startswith( 'comment' ):
                is_date_row = utils.is_date_spec( varname )
                #print 842048, row_number, column_vals
                for county, value, col_number in zip( counties, column_vals[1:], column_numbers ):
                    if value.strip():
                        county.add1( is_date_row, row_number, col_number, varname, value )
        for county in counties:
            county.tidy()
        Plot0(counties).draw()
        Plot1(counties).draw()
        Plot2(counties).draw()
        Plot3(counties).draw()

if __name__ == '__main__':
    main()
