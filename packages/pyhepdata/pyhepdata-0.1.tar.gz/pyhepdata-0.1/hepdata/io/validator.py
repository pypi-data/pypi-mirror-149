#!/usr/bin/env python3

"""Try to validate a submission file and possible data files

Author: Christian Holm Christensen <cholm@nbi.dk>

"""
import yaml
import json
import jsonschema
import os
import sys
import importlib
import copy
from . messages import Messages

# ====================================================================
class Validator(Messages):
    """Validates HepData files

    Parameters
    ----------
    schemadir : str (optional)
        Directory containing the schema files 
    
        - ``submission_schema.json`` 
        - ``data_schema.json`` 
        - ``additional_info_schema.json`` 
    
        If not specified, we try to find it via the ``importlib``
        interface by looking for the load path of
        ``hepdata_validator``

    """
    #: Indepdendent variables key 
    INDEPENDENT_VARIABLES = 'independent_variables'
    #: Depdendent variables key 
    DEPENDENT_VARIABLES = 'dependent_variables'
    #: Data file key 
    DATA_FILE = 'data_file' 
    #: Keywords key
    KEYWORDS = 'keywords'
    #: Description key
    DESCRIPTION = 'description'
    #: Name key
    NAME = 'name'
    #: Values key
    VALUES = 'values'

    #: Properties key
    PROPERTIES = 'properties'
    #: Required key
    REQUIRED = 'required'
    
    def __init__(self,schemadir=None,verb=False,compat=False):        
        super(Validator,self).__init__()
        self._check_res = True
        self._tables = {}
        self._verb   = verb
        
        try:
            if schemadir is None:
                spec = importlib.util.find_spec('hepdata_validator')
                schemadir = os.path.join(os.path.dirname(spec.origin),
                                         'schemas','1.0.1')
        except Exception as e:
            print('Failed to get directory to read schema from',
                  file=sys.stderr)

        self._sub_schema = self._readSchema(schemadir,
                                            'submission_schema.json')
        self._dat_schema = self._readSchema(schemadir,
                                            'data_schema.json')
        self._add_schema = self._readSchema(schemadir,
                                            'additional_info_schema.json')

        if compat:
            self._addRecords(self._sub_schema)
            self._addRecords(self._add_schema)
            self._addName(self._dat_schema)

    def _addRecords(self,schema):
        """Add the associated records to the schema for compatibility
        
        Parameters
        ----------
        schema : dict 
            The scheme to add to 
        """
        if schema is None:
            return
        
        if schema[self.PROPERTIES].get("associated_records",False):
            return 

        url = "http://jsonschema.net/associated_records"
        assoc = {
            "id": url+"",
            "type": "array",
            "description": "Links to other records.",
            "items": {
                "id": url+"/output",
                "type": "object",
                "properties": {
                    "type": {
                        "id": url+"/output/type",
                        "type": "string"
                    },
                    "identifier": {
                        "id": url+"/output/identifier",
                        "type": [
                            "string",
                            "number"
                        ]
                    },
                    "description": {
                        "id": url+"/output/description",
                        "type": "string"
                    },
                    "url": {
                        "id": url+"/output/url",
                        "type": "string"
                    }
                },
                "required": [
                    "identifier",
                    "type"
                ]
            }
        }
        schema[self.PROPERTIES]["associated_records"] = assoc
        
    def _addName(self,schema):
        """Add name to the schema for compatibility
        
        Parameters
        ----------
        schema : dict 
            The scheme to add to 
        """
        if schema is None:
            return

        if schema[self.PROPERTIES].get('name',False):
            return

        name =  {
            "id": "http://hepdata.org/submission/schema/data/name",
            "type": "string",
            "title": "Name.",
            "description":
            "Reference a data record when everything is in the same file.",
            "name": "name"
        }
        schema[self.PROPERTIES]["name"] = name
        
    def _readSchema(self,schemadir,filename):
        """Read in a schema 
        
        Parameters
        ----------
        schemadir : str 
            Directory to read the schema from 
        filename : str 
            Name of the file to read the schema from 
        
        Returns 
        -------
        schema : dict 
            The read schema 
        """
        if schemadir is None or schemadir == '':
            return None
        
        with open(os.path.join(schemadir,filename),'r') as inp:
            return json.load(inp)
        
    def _isTable(self,doc):
        """Check if read-in document is a table 
        
        Parameters
        ----------
        doc : dict 
            Read in document 
        
        Returns
        -------
        istable : bool 
            True if document is a data table 
        """
        return ((self.INDEPENDENT_VARIABLES in doc or
                 self.DEPENDENT_VARIABLES in doc))
    
    def _isMeta(self,doc):
        """Check if read-in document is table meta information (a submission
        entry)
        
        Parameters
        ----------
        doc : dict 
            Read in document 
        
        Returns
        -------
        ismeta : bool 
            True if document is table meta information

        """
        return (doc.get(self.DATA_FILE,False) or
                (doc.get(self.KEYWORDS,False) and
                 doc.get(self.DESCRIPTION,False) and
                 doc.get(self.NAME,False)))
    def validate(self,filename,data=None,**kwargs):
        """Validate a submission or data file 

        Parameters
        ----------
        filename : str 
            File name to validate - even if the data argument is
            supplied we must still give this argument.
        data : dict or None 
            Data to validate (a list of YAML docs).  Can be None, 
            in which case we open the file `filename`.  
        **kwargs : keyword arguments 
            - norecourse : bool 
                If False, do not recourse to other files 

        Returns
        -------
        ret : bool 
            True on success

        """
        norec    = kwargs.pop('norecurse',False)
        
        # Check argument 
        if filename is None:
            raise LookupError('The filename is mandatory')

        if self._verb:
            print('Validating {}'.format(filename))
                  
        try:
            # Check if we have data 
            if data is None:
                if self._verb:
                    print('Reading in {}'.format(filename))

                data = yaml.load_all(open(filename,'r'),
                                     Loader=yaml.SafeLoader)

                # Make a list (from generator) of documents
                data = list(data)

            if type(data) is dict:
                data = [data]
                
            # Loop over documents in data to extract tables.
            # We build a dictonary from table name to data table document
            for doc in data:
                # Check for empty document 
                if doc is None:
                    continue

                if (self._isTable(doc) and not self._isMeta(doc)):
                    if self._verb:
                        print('Found data table {} in {}'
                              .format(doc[self.NAME],filename))

                    self._tables[doc.get(self.NAME,'')] = doc
                
            # Loop over documents in data
            if self._verb:
                print("Looping over documents in {}".format(filename))
                
            for doc in data:
                # Check for empty document 
                if doc is None:
                    continue

                if self._verb:
                    print('Check a document')
                    
                try:
                    # If the document has the field 'data_file', it is
                    # a submission (table meta data) entry
                    #
                    # If the document has the field
                    # 'independent_variables', then it is a data table
                    # entry
                    #
                    # If neither of those fields are found, we assume
                    # that we have additional information in the
                    # document
                    #
                    if self._isMeta(doc):
                        self.validateSub(filename,doc,norec)
                    elif self._isTable(doc):
                        self.validateDat(filename,doc)
                    else:
                        self.validateAdd(filename,doc)

                except jsonschema.ValidationError as ve:
                    if self._verb:
                        print(ve)

                    from pprint import pformat
                    self.addError(filename,
                                   ve.message+' in\n'+
                                   pformat(ve.instance,compact=True))

            return not self.hasErrors()

        except yaml.scanner.ScannerError as e:
            if self._verb:
                print('Scanning error: {}'.format(e))
            self.addError(filename,
                             'Problem parsing file.\n'
                             + str(e))

        # except Exception as e:
        #    if self._verb:
        #        print('General exception: {}'.format(e))
        #    self.addError(filename, str(e))

        return False

    def validateFile(self,filename,location):
        if not self._check_res:
            if self._verb:
                print('skip')

            return True

        location = os.path.join(os.path.dirname(filename),location)
        ret = os.path.isfile(location)

        if self._verb:
            print('ok' if ret else 'bad')

        return ret
        
    def validateRes(self,filename,doc):
        """Validates additional resources

        Parameters
        ----------
        filename : str 
            Current filename 
        doc : dict 
            Current YAML document 
        """
        if self._verb:
            print('Validating additional resources')
            
        for resource in doc.get('additional_resources',[]):
            location = resource.get('location','')
            if self._verb:
                print(' additional resource: {} '.format(location),end='')

            if location.startswith('http'):
                # Do not check external resources
                continue

            if not self.validateFile(filename,location):
                  self.addWarning(filename,'Resource {} not found'
                                   .format(location))
                  if self._verb:
                      print(os.getcwd())
                      
            if '/' in location:
                  self.addWarning(filename,
                                  'Resource {} should not contain "/"'
                                  .format(location))
            
                            
    def validateSub(self,filename,doc,norec):
        """Validates a submission file entry (table meta data)

        Parameters
        ----------
        filename : str 
            Current filename 
        doc : dict 
            Current YAML document 
        """
        if self._verb:
            print('Validating submission entry {}'
                  .format(doc.get(self.NAME,'')))

        # The schema to use 
        schema = self._sub_schema
        single = (doc.get(self.DATA_FILE,'') == '' or 
                  doc.get(self.INDEPENDENT_VARIABLES,False) or
                  doc.get(self.DEPENDENT_VARIABLES,False))
        if single:
            if self._verb:
                print('Got new-style one-document submission')
                
            # Set the document field data_file to the empty string
            doc = dict(doc,**{self.DATA_FILE:''})
        
        if schema is not None:
            # If the document does not contain the field data_file, or it
            # contains either of independent_variables or
            # dependent_variables, then we amend the schema include the
            # data file schema.
            if single:
                if self._verb:
                    print('Got new-style one-document submission')

                # Merge properties of submission and data schema 
                props = dict(self._sub_schema[self.PROPERTIES],
                             **self._dat_schema[self.PROPERTIES])
                schema = copy.deepcopy(schema)
                schema[self.PROPERTIES] = props
                # Add stuff to required fields
                schema[self.REQUIRED] += self._dat_schema[self.REQUIRED]
                norec = True
            
            # This throws in case of errors - handled one level up 
            jsonschema.validate(doc,schema)
        else:
            self.addWarning(filename,'No meta schema available')

        # Validate additional resources in the document
        self.validateRes(filename,doc)
        
        # Now check the data file if not part of this file
        if doc[self.NAME] not in self._tables:
            # We haven't seen the data file yet, so we check it here 
            df = doc[self.DATA_FILE]

            # Check sanity of file path
            if '/' in df:
                self.addWarning(filename,
                                'Data file names should not contain "/": {}'
                                .format(df))

            if not norec:
                rdf = os.path.join(os.path.dirname(filename),df)
                ret = self.validate(filename=rdf,data=None)

        self.addInfo(filename,"Contains the valid submission {}"
                     .format(doc[self.NAME]))

        
    def validateDat(self,filename,doc):
        """Validate data entry (a table)

        Parameters
        ----------
        filename : str 
            Current filename 
        doc : dict 
            Current YAML document 
        """
        if self._verb:
            print('Validating data entry {} in {}'
                  .format(doc.get(self.NAME,''),filename))
            
        # This raises in case of problems - handled one level up
        if self._dat_schema is not None:
            jsonschema.validate(doc,self._dat_schema)
        else:
            self.addWarning(filename,'No data schema available')

        len_indep = [len(i[self.VALUES])
                     for i in doc[self.INDEPENDENT_VARIABLES]
                     if len(i[self.VALUES]) > 0]
        len_dep   = [len(d[self.VALUES])
                     for d in doc[self.DEPENDENT_VARIABLES]]
        
        if len(set(len_indep+len_dep)) > 1:
            # If we have one or more unique counts, it's a problem
            self.addWarning(filename,"Inconsistent lengths of independent "
                            "variables {} and dependent variables {}"
                            .format(str(len_indep),str(len_dep)))

        self.addInfo(filename,"Contains a valid data table {}"
                      .format(doc.get(self.NAME,'')))

    def validateAdd(self,filename,doc):
        """Validate additional information (header)

        Parameters
        ----------
        filename : str 
            Current filename 
        doc : dict 
            Current YAML document 
        """
        if self._verb:
            print('Validating header entry')
            
        # This raises in case of problems - handled one level up
        if self._add_schema is not None:
            jsonschema.validate(doc,self._add_schema)
        else:
            self.addWarning(filename,'No submission schema available')
        
        # Validate additional resources in the document
        self.validateRes(filename,doc)
        
        self.addInfo(filename,"Contains valid additional information")
            
if __name__ == "__main__":
    import argparse as ap
    import sys
    
    def check_dir(val):
        if not os.path.isdir(val):
            raise ap.ArgumentTypeError('{} is not a directory'
                                       .format(val))
        return val

    parser = ap.ArgumentParser(description="Validates HepData files")
    parser.add_argument('input',
                        type=ap.FileType('r'),
                        help='File to parse',
                        default='submission.yaml')
    parser.add_argument('-v',
                        '--verbose',
                        dest='verbose',
                        action='store_true',
                        help='Be verbose')
    parser.add_argument('-q',
                        '--quiet',
                        dest='verbose',
                        action='store_false',
                        help='Be quiet')
    parser.add_argument('-l',
                        '--level',
                        default='WARNING',
                        choices=['INFO','WARNING','ERROR'],
                        help='Level of output')
    parser.add_argument('-s',
                        '--schema',
                        type=check_dir,
                        help='Location of schema files')
    parser.set_defaults(verbose=False)
    
    args = parser.parse_args()

    lvl = getattr(Message, args.level)

    v = Validator(args.schema,
                  verb=args.verbose)

    v.validate(file_path=args.input.name,
               data=None)
    v.summarize(lvl)
    e = v.hasErrors(None)
    if e or v.hasWarnings(None):
        v.printMessages(None,Message.WARNING)
        if e:
            print('There was a problem')
            sys.exit(1)

# ====================================================================
#
# EOF
#
