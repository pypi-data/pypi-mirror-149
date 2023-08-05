# NOTES

## MAIN TODOs

URIs
  Resource_name can specify the name of an input or output, and that can be mapped via a spec, and ModelRunner will help
  you build such a spec.

  Or it can just be a filename or a URI.  If you point at a service that requires credentials you have to supply the 
  credentials in kwargs.

  You can specify both resource_name and 'uri', in which case uri is just a default, and the name can be overridden.

  'filesystem' - get_filesystem(), get_sql_connection()


DSW remote use case -- need dslibrary implementation of REST

Upload to s3 -- can't append, need to use native multi-part upload (or just accumulate locally then send - cheap!)

* other ways to use dslibrary with notebooks
  - maybe: notebook arguments
  
* in DSW use case
  - keep using mmlibrary?
  - need to support dsw:// protocol handler
  - support "local_file"
  - how do we support mapping of inputs???
  - why do we need to make a REST call for every file read?

* connect to DSW use case
  - definitely don't want to use mmlibrary here
  - need dsw://...
  - need "local_file" to map to remote files

* Unit test that works through the 'delivered environment' use case -- see ModelRunner.prepare_run_env()
  
* mmlibrary use case: there isn't any way to send file format information, and it isn't documented
  * for local testing we would use ModelRunner() -- that needs testing
  * for execution in run-in-dsw, we can adjust parameters but there's no section for selecting inputs & outputs
    (we used to have a mapping section, but that's not exactly the same)
  * for run-in-mm, we would need to be able to send environment variables to configure the format/data sources

* get_metadata() and MLProject are not described anywhere yet, and the rationale for having this included needs to be
  explained.
    * documents the entry points
    * parameter names & defaults
    * schemas will be very useful later; we'll add validation methods
    * gives us deeper compatibility with MLFlow


## DOCUMENTATION TODOs

* demonstrations for connection to s3, abs, postgres, etc..  (document all the kwargs)

* how the abstraction works:
  * caller packs up all the specs (ModelRunner)
  * those can go into an environment variable
  * the specification configures a DSLibrary instance
  * the model code now has access to all the data, with all of its settings
  * the model can be isolated from the credentials/etc. in various ways


## How to Upload to PyPi

NOTE: 'twine' is required:
    
    pip install twine

### 1) increment version number

In setup.py and in dslibrary/__init__.py.

This is currently done manually but there is a tool called 'bumpversion' that might automate this:
    https://realpython.com/pypi-publish-python-package/

### 2) remove old version

    rm dist/*

### 3) build

    python setup.py sdist bdist_wheel

### 4) upload (prompts for PyPi username and password)

    twine upload dist/*
