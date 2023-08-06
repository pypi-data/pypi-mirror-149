# VAIP (Virtual Archive Information Package) Models Overview
This is a central repository for VAIP CRUD (create, read, update, and delete) operations for the various types of AIPs
we manage. This includes AIUs (Archival Information Units), which are generally associated with granules, and 
AICs (Archival Information Collections), which are generally associated with collections and higher level groupings. 
We can use AICs to represent collections of collections or subsets thereof. This is a many-to-many 
system of relationships. 

## Package Description
The package entails VAIP generation located in the vaip.kg directory.

### vaip.kg
vaip.kg is an rdflib based implementation which connects to a AWS Neptune knowledge graph store to run SPARQL queries in order to perform CRUD operations on the vAIP.

## Installation
While under the `vaip` directory,

* `python setup.py install` or `pip install .\vaip\`
* `pip install -r requirements.txt`

##### Local s3 Testing
* `export AWS_TEST_LOCAL="true"` # sets url for local vs VPC
* `export AWS_TEST_PROFILE="your-aws-profile"` # only if not running in VPC (locally)

Updates to vaip are handled by sam deploy of the system.

## Documentation to update ontology .owl file 
The ontology is located in the data subfolder.

- Download the latest ontology file from webprotege (RDF/XML)
- Make a copy with a new version increasing bugfix, minor, and then major version number-
- Upload the file into webprotege 
- Upload .owl file to Amazon S3 **"ncap-archive-dev-pub/vaip"**
	 - **S3 url https://s3.console.aws.amazon.com/s3/buckets/ncap-archive-dev-pub?region=us-east-1&prefix=vaip/&showversions=false**

	
## The vaip package should be updated on PyPi
To update the package, you will need to register for a PyPi account.

To build the package for upload:
- Update version in __init__.py and setup.py
- python setup.py sdist

Next install twine (one time setup)

- pip install twine
- twine upload dist/*

To test out the package
- pip install ncap-vaip


last updated 01-18-2022