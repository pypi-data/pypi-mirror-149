"""A small utility class for converting ROOT objects (:class:`TH1`,
:class:`TGraphAsymmErrors`, :class:`TGraphErrors`, and
:class:`TMultiGraph`) into HEPData format 

Copyright 2019 Christian Holm Christensen
"""
import numpy as np
try:
    from ROOT import TH1, TGraphAsymmErrors, TGraphErrors, TMultiGraph
except:
    print('ROOT Python interface not available')


class ToHEPData:
    """A small utility class for converting ROOT objects (:class:`TH1`,
    :class:`TGraphAsymmErrors`, :class:`TGraphErrors`, and
    :class:`TMultiGraph`) into HEPData format 

    The method :meth:`ToHEPData.getData` extracts the data from an
    object of one of the classes above and returns a 2D NumPy array
    where each row has the format

    .. math::
        
        x_l,x_h,x,y,[(\delta_y^{-},\delta_y^{+}),\dots]

    where :math:`x_l,x_h` is the bounds on the independent variable,
    and :math:`x` is the value, :math:`y` is the value of the
    dependent variable, and
    :math:`[(\delta_y^{-},\delta_y^{+}),\dots]` is any number of
    uncertainties given as lower and upper values

    This array can then be passed to :meth:`ToHEPData.fillIn` together
    with the independent and dependent column objects to fill in all
    values and uncertainties.

    """
    def __init__(self):
        pass

    @classmethod
    def getH1Data(cls,h):

        """Extract data from a 1D histogram 

        Parameters
        ----------
        h : TH1
            Histogram to extract the data from 
        
        Returns
        -------
        data : numpy.ndarray 
            The read data.   Each row has the format 

            .. math::
        
                x_{\mathrm{low}},x_{\mathrm{high}},x,y,\delta_y^{-|,\delta_y^{+}
        
            Thus we can pass this more or less directly on to a table 
        """
        return np.array([[h.GetXaxis().GetBinLowEdge(i),
                          h.GetXaxis().GetBinUpEdge(i),
                          h.GetXaxis().GetBinCenter(i),
                          h.GetBinContent(i),
                          h.GetBinErrorLow(i),
                          h.GetBinErrorUp(i)]
                         for i in range(h.GetNbinsX())])

    @classmethod 
    def getAsymData(cls,a):
        """Extract data from a graph with asymmetric errors

        Parameters
        ----------
        a : TGraphAsymmErrors
            Graph to extract the data from 
        
        Returns
        -------
        data : numpy.ndarray 
            The read data.   Each row has the format 

            .. math::
        
                x-\delta_x^{-},x+\delta_x^{+},x,y,\delta_y^{-},\delta_y^{+}
        
            Thus we can pass this more or less directly on to a table 
        """
        return np.array([[x-exl,x+exh,x,y,eyl,eyh]
                         for x,exl,exh,y,eyl,eyh in zip(a.GetX(),
                                                        a.GetEXlow(),
                                                        a.GetEXhigh(),
                                                        a.GetY(),
                                                        a.GetEYlow(),
                                                        a.GetEYhigh())])

    @classmethod
    def getSymData(cls,s):
        """Extract data from a graph with errors

        Parameters
        ----------
        a : TGraphErrors
            Graph to extract the data from 
        
        Returns
        -------
        data : numpy.ndarray 
            The read data.   Each row has the format 

            .. math::
        
                x-\delta_x,x+\delta_x,x,y,\delta_y,\delta_y
        
            Thus we can pass this more or less directly on to a table 
        """
        return np.array([[x-ex,x+ex,x,y,ey,ey]
                         for x,ex,y,ey in zip(s.GetX(),
                                              s.GetEX(),
                                              s.GetY(),
                                              s.GetEY())])

    @classmethod
    def getMultiData(cls,l):
        """Extract data from the list of objects passed in. 
        
        Parameters
        ----------
        l : iterable
            List of objects to extract data from 

            The first object is assumed to set the data point values 

            .. math::
        
                (x^{+\delta_x^{+}}_{-\delta_x^{-}},y)

            and the first set of uncertainties on the dependent
            variable :math:`y`.  Remaining objects are expected to set
            additional uncertainties.  Note, the input objects should
            all have the same :math:`x` and :math:`y` values
            (checked).

        Returns
        -------
        data : numpy.ndarray 
            The read data.   Each row has the format 

            .. math::
        
                x-\delta_x^{-},x+\delta_x^{+},x,y,\delta_y^{-},\delta_y^{+}
        
            Thus we can pass this more or less directly on to a table 
        """
        ds = [cls.getData(i) for i in l]
        f  = ds[0]
        for o in ds[1:]:
            assert np.allclose(f[:,0],o[:,0]),'Incompatible X values'
            assert np.allclose(f[:,3],o[:,3]),'Incompatible Y values'
            print(f.shape,o[:,4:].shape)
            f = np.hstack((f,o[:,4:]))

        return f

    @classmethod
    def getData(cls,o):

        """Get data from an object.  The object can be one of 

        - TH1
        - TGraphErrors
        - TGraphAsymmErrors
        - TMultiGraph 
        
        If a TMultiGraph is passed in, then we assume that the first
        graph contains the data points :math:`(x,y)` and possibly
        uncertainties.  The remaining graphs are assumed to only have
        additional uncertainties

        Parameters
        ----------
        o : object 
            Object to read the data from 

        Returns
        -------
        data : numpy.ndarray 
            The read data.   Each row has the format 

            .. math::
        
                x-\delta_x^{-},x+\delta_x^{+},x,y,\delta_y^{-},\delta_y^{+}
        
            Thus we can pass this more or less directly on to a table 
        """
        if isinstance(o,TH1):
            return cls.getH1Data(o)
        if isinstance(o,TGraphAsymmErrors):
            return cls.getAsymData(o)
        if isinstance(o,TGraphErrors):
            return cls.getSymData(o)
        if isinstance(o,TMultiGraph):
            return cls.getMultiData(o.GetListOfGraphs())

        return None

    @classmethod
    def fillIn(cls,x,y,d):
        """Fills in the values in `d` in the independent (`x`) and
        dependent (`y`) variable columns, along with any uncertainties. 

        Parameters
        ----------
        x : hepdata.Independent 
            The column for the independent variable 
        y : hepdata.Dependent 
            The column for the dependent variable 
        d : The data to fill in.  Each row of this should have the format 

            .. math::
        
                x_l,x_h,x,y,[(\delta_y^{-},\delta_y^{+}),\dots]

            where :math:`x_l,x_h` is the bounds on the independent
            variable, and :math:`x` is the value, :math:`y` is the
            value of the dependent variable, and
            :math:`[(\delta_y^{-},\delta_y^{+}),\dots]` is any number
            of uncertainties given as lower and upper values

        Returns
        -------
        hmm
        """
        _,ncol = d.shape
        assert ncol >= 4, 'Too few columns passed in for data'
        assert ncol % 2 == 0, 'Not even number of columns'
        
        x.value(d[:,0],d[:,1],d[:,2])
        vl = y.value(d[:,3])
        for i,j in zip(range(4,ncol,2),range(5,ncol,2)):
            # We use Value.asymerror as this will call Value.symerror
            # in case the values are close.
            vl.asymerror(d[:,i],d[:,j])

#
# EOF
#
