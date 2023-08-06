# XML Rollbasase To GIT

App that changes an XML Rollbase application into a git repository.

### Features
- xml conversion
- git history relative to the creation date of the XML file
- git push
- branch creation for each customer when `-c` parameter is set


## Requires
see [requirement.txt](requirements.txt)


##  Installation
`pip install xmlib-to-git`


## Usage
```bash
$ xmlib-to-git \
-f <xml-file> \
-o <local-repo> \
[-g <remote-repo] \
[-c <customer-id] \
[-v]
```
