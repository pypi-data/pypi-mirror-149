"""A container of mesages 

Copyright 2019 Christian Holm Christensen
"""
# ====================================================================
class Message:
    """Container of messages with a severity level"""
    ERROR = 2
    WARNING = 1
    INFO = 0
    
    def __init__(self,filename='',message='',level=None):
        """Create a message for a file and a specific severity level"""
        self._file    = filename
        self._level   = level
        self._message = message
        self._tables  = {}
        if self._level is None:
            self._level = self.ERROR

    @classmethod
    def levelStr(cls,lvl):
        """Stringify severity level"""
        return ("Error"   if lvl == cls.ERROR else
                "Warning" if lvl == cls.WARNING else
                "Info"    if lvl == cls.INFO else
                "Unknown")
    
    def __str__(self):
        """Get string representation"""
        return "{:10s} - {}".format(Message.levelStr(self._level),
                                    self._message)

# ====================================================================
class Messages:
    """Container of messages"""
    def __init__(self):
        self._messages = {}

    def _ensureMessages(self,filename):
        """Ensure we have an entry for ``filename``"""
        if filename not in self._messages:
            self._messages[filename] = []

        return self._messages[filename]
        
    def addError(self,filename,message):
        """Add a message to the output

        Parameters
        ----------
        filename : str
            Current filename
        message : str
            Content of the message 
        """
        self._ensureMessages(filename)\
            .append(Message(filename,message,Message.ERROR))

    def addWarning(self,filename,message):
        """Add a message to the output

        Parameters
        ----------
        filename : str
            Current filename
        message : str
            Content of the message 
        """
        self._ensureMessages(filename)\
            .append(Message(filename,message,Message.WARNING))
        
    def addInfo(self,filename,message):
        """Add a message to the output

        Parameters
        ----------
        filename : str
            Current filename
        message : str
            Content of the message 
        """
        self._ensureMessages(filename)\
            .append(Message(filename,message,Message.INFO))

    def _filterMessages(self,filename,least,exact=False):
        """Filter messages that belong to ``filename``

        Parameter
        ---------
        filename : str 
            Filename to search for messages for 
        least : int 
            The least error level to get messages for 
        exact : bool
            Match the exact error level 
        
        Returns
        -------
        messages : list 
             List of messages found
        """
        return [m for m in self._ensureMessages(filename)
                if (m._level == least and exact) or 
                (m._level>=least and not exact)]
                
    def getMessages(self,filename=None,least=None,exact=False):
        """Get messsages for a given filename or all messages
        
        Parameter
        ---------
        filename : str 
            Filename to search for messages for. If None, return all
            messages at the given level
        least : int 
            The least error level to get messages for 
        exact : bool
            Match the exact error level 
        
        Returns
        -------
        messages : list 
             List of messages found

        """
        if filename is None:
            if least is None:
                return self._messages;

            ret = {}
            for f in self._messages:
                ret[f] = self._filterMessages(f,least,exact)
            return ret

        if least is None:
            return self._ensureMessages(filename)
        return self._filterMessages(filename,least,exact)

    def clearMessages(self):
        """Reset messages"""
        self._messages = {}

    def hasErrors(self,filename=None):
        """Check if a file has errors

        Parameters
        ----------
        filename : str 
            Filename to assert on 
        
        Returns
        -------
            ret : bool 
                True if there's any errors associated with ``filename``
        """
        if filename is None:
            for f in self._messages:
                if self.hasErrors(f):
                    return True
            return False
        
        return len(self.getMessages(filename,Message.ERROR,exact=True)) > 0

    def hasWarnings(self,filename):
        """Check if a file has warnings

        Parameters
        ----------
        filename : str 
            Filename to assert on 
        
        Returns
        -------
            ret : bool 
                True if there's any warnings associated with ``filename``
        """
        return len(self.getMessages(filename,Message.WARNING,exact=True)) > 0

    def printMessages(self,filename=None,least=Message.INFO):
        """Print all errors associated with a file 
        
        Parameter
        ---------
        filename : str 
            Filename to search for messages for. If None, return all
            messages at the given level
        least : int 
            The least error level to get messages for 
        """
        if filename is None:
            for f in self._messages:
                self.printMessages(f,least)
            return

        m = self.getMessages(filename,least)
        if len(m) <= 0 and least > Message.INFO:
            return
        
        print(filename)
        for e in m:
            print("\t{}".format(e.__str__()))

    def summarize(self,least=Message.INFO,filename=None):
        """Summarize findings

        Parameter
        ---------
        least : int 
            The least error level to get messages for 
        """
        if least > Message.INFO:
            return
        
        for f in self._messages:
            if filename is not None and f != filename:
                continue
            print('{}'.format(f),end='')

            e = self.hasErrors(f)
            w = self.hasWarnings(f)

            print(' {}'.format('has warnings' if w else
                               'is clean'),end='')
            print(' {}'.format('but' if (not w and e) or (w and not e) else
                                'and'),end='')
            print(' {}'.format('has errors' if e else
                               'is valid'))
    
    
#
# EOF
#
