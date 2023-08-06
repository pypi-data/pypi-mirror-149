"""Utility class with uncertainty propagators 

Copyright 2019 Christian Holm Christensen
"""
import math
from . combiner import LinearSigma, LinearVariance, Adder2

class Propagator:
    """Utility class with uncertainty propagators"""
    #: Symmetric error (sic) field name 
    SYMERROR = 'symerror'
    #: Asymmetric error (sic) field name 
    ASYMERROR = 'asymerror'
    #: Plus field name 
    PLUS = 'plus'
    #: Minus field name 
    MINUS = 'minus'
    #: Label field name 
    LABEL = 'label'

    @classmethod
    def _val(cls,strorfloat,value):
            
        try:
            return float(strorfloat)
        except:
            pass

        if type(strorfloat) is str and strorfloat.endswith('%'):
            v = float(value)
            return v * float(strorfloat[:-1])/100

    @classmethod
    def asis(cls,errors,value,**kwargs):
        """Default function to extract uncertainty values.  

        This simply maps the symmetric uncertainties to a scalar, 
        and asymmetric uncertainties to a tuple of 2 values 
        
        Parameters
        ----------
        errors : list 
            List of uncertainties to process 
        value : float (not used)
            Point value
        **kwargs : keyword arguments
            Other arguments 
            - defval : Default value (math.nan)

        Returns
        -------
        err : list 
            List of scalars and 2-tuples 
        delta : float 
           Shift on value (always 0)
        """
        defval = kwargs.get('default',math.nan)
        def conv(e):
            if cls.ASYMERROR in e:
                p = e.get(cls.ASYMERROR,{})
                return (cls._val(p.get(cls.MINUS,defval),value),
                        cls._val(p.get(cls.PLUS, defval),value))
            
            if cls.SYMERROR in e:
                return cls._val(e.get(cls.SYMERROR,defval),value)

            return defval

        return list(map(conv,errors)),0

    @classmethod
    def sumsq(cls,errors,value,**kwargs):
        """Extract total uncertainty by taking the square root of 
        the sum of squares.  

        Note, asymmetric uncertainties are not supported.  If you use
        this on a value with asymmetric uncertainties, it will raise
        an exception.  Use linvar or linstd instead. 
        
        Parameters
        ----------
        errors : list 
            List of uncertainties to process 
        value : float
            Not used 
        **kwargs : keyword arguments
            Other arguments 
            - defval : Default value (math.nan)

        Returns
        -------
        err : float 
            The total uncertainty
        delta : float 
           Shift on value (always 0)
        """
        defval = kwargs.get('default',math.nan)
        pairs  = kwargs.get('alswaystuple',False)
        def sq(e):
            if cls.ASYMERROR in e:
                raise ValueError('Asymmetric uncertainties can not be added '
                                 'in quadrature')
            if cls.SYMERROR in e:
                return cls._val(e.get(cls.SYMERROR,defval),value)**2
            return 0

        return math.sqrt(sum(map(sq,errors))),0

    @classmethod
    def _model(cls,model,errors,value,**kwargs):
        """Extract total uncertainty by using a combiner.
        
        Parameters
        ----------
        model : object 
            The model to use 
        errors : list 
            List of uncertainties to process 
        value : float
            Not used         
        **kwargs : keyword arguments
            Other arguments 

        Returns
        -------
        err : float 
            The total uncertainty
        delta : float
            Adjustment to value 
        """
        defval = kwargs.get('default',math.nan)
        a = Adder2(model)
        for e in errors:
            if cls.ASYMERROR in e:
                p = e.get(cls.ASYMERROR,{})
                # Note the sign change on the low error.  HepData
                # assumes that a _negative_ low uncertainty reflects a
                # lower bound _smaller_ than the value, but the
                # combiner framework assumes the opposite (positive
                # low value is a lower bound _smaller_ than the
                # value).  Thus, we flip the sign here.
                a.add(0,
                      -cls._val(p.get(cls.MINUS,defval),value),
                      cls._val(p.get(cls.PLUS,defval),value))
            elif cls.SYMERROR in e:
                v = cls._val(e.get(cls.SYMERROR,defval),value)
                a.add(0,v,v)

        l, h, dx = a()
        # Note, we flip the sign on the lower bound again, as
        # explained in the comment above.
        return (-l,h),dx
        
    @classmethod
    def linstd(cls,errors,value,**kwargs):
        """Extract total uncertainty by using a linear sigma combiner,
        appropriate if some of the uncertainties may be correlated.
        This will then provide an upper bound estimate on the total
        uncertainty.

        This also works for asymmetric uncertainties 
        
        Parameters
        ----------
        errors : list 
            List of uncertainties to process 
        value : float
            Not used 
        **kwargs : keyword arguments
            Other arguments 

        Returns
        -------
        err : float 
            The total uncertainty
        delta : float
            Adjustment to value 

        """
        return cls._model(LinearSigma,errors,value,**kwargs)

    @classmethod
    def linvar(cls,errors,value,**kwargs):
        """Extract total uncertainty by using a linear variance combiner,
        appropriate all the uncertainties are uncorrelated.

        This also works for asymmetric uncertainties 
        
        Parameters
        ----------
        errors : list 
            List of uncertainties to process 
        value : float
            Not used 
        **kwargs : keyword arguments
            Other arguments 

        Returns
        -------
        err : float 
            The total uncertainty
        delta : float
            Adjustment to value 
        """
        return cls._model(LinearVariance,errors,value,**kwargs)

    @classmethod 
    def withlabel(cls,errors,value,*,label_calc,labels,**kwargs):
        """Filter what errors to include based on the labels. 
        
        The argument labels can be a callable, a single string, or a
        iterable of strings. Passing the empty string as an element
        will allow for unlabeled errors.

        This function does not calculate the actual value.  Instead
        that calculation is delegated to the callable f which must
        have a signature like

        >>> label_calc(errors,value,defval) -> any

        The calculator function label_calc can for example be
        Propagator.sumsq, Propagator.linvar, Propagator.linstd, or
        some other user-defined function.

        Examples
        --------
        
        With a list of strings 

        >>> a = Value(12.3456)
        >>> e = [1.23456, 0.123456, 0.0123456, 10]
        >>> l = ['a', 'b', 'c', 'd']
        >>> for ee,ll in zip(e,l):
        ...    a.symerror(ee,ll)
        ...
        >>> res = a.e(Propagator.withlabel,
        ...           label_calc=Propagator.sumsq,
        ...           labels=['a','b','c'])

        With a single string 

        >>> res = a.e(lambda errors,value :
        ...            Propagator.withlabel(errors,value,
        ...                                label_calc=Propagator.sumsq,
        ...                                labels='a'))

        With a callable 

        >>> res = a.e(Propagator.withlabel,
        ...           label_calc=Propagator.sumsq,
        ...           labels=lambda l : l != 'a')

        If this is to be used with other filters, such as
        Propagator.stack, then this should probably be the first
        specified calculator, for example

        >>> a = Value(12.3456)
        >>> e = [1.23456, 0.123456, 0.0123456, 10]
        >>> l = ['a', 'b', 'c', 'd']
        >>> for ee,ll in zip(e,l):
        ...     a.symerror(ee,ll)
        >>> res = a.e(Propagator.withlabel, labels=['a','b','c'],
        ...           label_calc=Propagator.stack,
        ...           stack_calc=Propagator.sumsq)
                    
        Parameters
        ----------
        label_calc : callable 
            A callable to calculate the result e.g., 
            Propagator.sumsq 
        labels : callable, str, list 
            Either 
                - A callable that returns true if an error should be
                  included,
                - A single string value that the error labels must
                  match, or
                - An iterable for which the error labels must match at
                  least one element.
        errors : list 
            List of the errors 
        value : float 
            Point value 
        **kwargs : keyword arguments
            Other arguments 

        Returns
        -------
        res : float, (float,float) or list
            Result of applying f to the selected errors
        delta : float
            Adjustment to value 
        """
        if label_calc is None:
            label_calc = cls.asis

        assert callable(label_calc), "Passed calculator not a callable"
        
        if callable(labels):
            ff = lambda l : labels(l.get(cls.LABEL))
        elif isinstance(labels,str):
            ff = lambda l: l.get(cls.LABEL,'') == labels
        else:
            ff = lambda l : l.get(cls.LABEL,'') in labels

        # We convert from generator to list so that the calculator can
        # access the values multiple times if needed.
        return label_calc(list(filter(ff,errors)),value,**kwargs)


    @classmethod
    def stack(cls,errors,value,*,stack_calc,**kwargs):
        """Return a list of uncertainties where the succiently stack up to
        build up the final uncertainty.

        This function does not calculate the actual value.  Instead
        that calculation is delegated to the callable stack_calc which
        must have a signature like

        >>>  stack_calc(errors,value,**kwargs) -> scalar or (scalar,scalar) 

        Note that the callable stack_calc must return either a single
        value or a pair of singular values

        Examples
        --------
        
        >>>       a = Value(1)
        >>>       for i in range(1,5):
        ...           a.symerror(1)
        >>>       res = a.e(Propagator.stack,stack_calc=Propagator.sumsq)
           
        If this is to be used with other filters, such as
        Propagator.withlabel, then this should probably be the second
        to last specified calculator, for example

        >>> a = Value(12.3456)
        >>> e = [1.23456, 0.123456, 0.0123456, 10]
        >>> l = ['a', 'b', 'c', 'd']
        >>> for ee,ll in zip(e,l):
        ...     a.symerror(ee,ll)
    
        >>> res = a.e(Propagator.withlabel, labels=['a','b','c'],
        ...           label_calc=Propagator.stack,
        ...           stack_calc=Propagator.sumsq)

        Parameters
        ----------
        stack_calc : callable 
            A callable to calculate the result e.g., 
            Propagator.sumsq 
        errors : list 
            List of the errors 
        value : float 
            Point value 
        **kwargs : keyword arguments
            Other arguments 

        Returns
        -------
        res : float, (float,float) or list
            Result of applying f to the selected errors
        delta : float
            Adjustment to value 

        """
        if stack_calc is None:
            stack_calc = cls.sumsq
            
        assert callable(stack_calc), "Passed calculator not a callable"

        off = 0
        def update(last):
            # Exlicit side effect
            nonlocal off
            r,off = stack_calc(errors[:last+1], value, **kwargs)
            # print(errors[:last+1],r,off)
            return r

        r = list(map(update,range(len(errors)))), off
        # print(r,off)
        return r

    @classmethod
    def center(cls,errors,value,*,center_calc,**kwargs):
        """Centres data point in uncertainties thereby setting symmetric
        uncertainties.

        This function does not calculate the actual value.  Instead
        that calculation is delegated to the callable `center_calc`
        which must have a signature like

        >>>  center_calc(errors,value,**kwargs) -> scalar or (scalar,scalar) 

        Note that the callable center_calc must return either a single
        value or a pair of singular values

        Examples
        --------
           
        If this is to be used with other filters, such as
        Propagator.withlabel, then this should probably be the second
        to last specified calculator, for example

        >>> a = Value(12.3456)
        >>> e = [1.23456, 0.123456, 0.0123456]
        >>> for ee in e: a.asymerror(-ee-+.1,ee)
        >>> res = a.e(Propagator.center, 
        ...           center_calc=Propagator.linvar)


        Parameters
        ----------
        center_calc : callable 
            A callable to calculate the result e.g., 
            Propagator.sumsq 
        errors : list 
            List of the errors 
        value : float 
            Point value 
        **kwargs : keyword arguments
            Other arguments 

        Returns
        -------
        res : float, (float,float) or list
            Result of applying f to the selected errors
        delta : float
            Adjustment to value 

        """
        if center_calc is None:
            center_calc = cls.sumsq
            
        assert callable(center_calc), "Passed calculator not a callable"

        r,off = center_calc(errors, value, **kwargs)
        try:
            len(r)
            off += (r[1]+r[0]) / 2
            r   =  (r[1]-r[0]) / 2;
        except Exception as e:
            print(f'Cannot take length of {r}: {e}')
            pass

        return r,off
#
# EOF
#
