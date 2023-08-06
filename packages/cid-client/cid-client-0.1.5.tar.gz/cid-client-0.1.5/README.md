# Client for Coherent Identifier Tool

Wrapper for [CID Tool GraphQL API](https://github.com/coherentdigital/coherent-identifier/tree/cid-oleg-new/cid_tool).

## Usage

    pip install cid-client    
    
## Authentication

Basic (login/password) authentication with limited number of service users is currently used in CID Tool.
Service and test credentials are available in AWS SecretManager.

```python
from cid_client import CIDClient
cid_client = CIDClient(environment='dev')
cid_client.authenticate_basic('<your login>', '<your password>') # Paste real credentials here
```

Access token is then used for any Create/Update of the CID.


## Code examples

Find all examples: [here](examples).

**CID create:**

```python
cid_input = CreateCIDInput(
    who=PersonOrThingInput(
        thing=ThingInput(
            name='CID Client'
        )
    ),
    location=LocationInput(
        artifact='https://www.planetebook.com/free-ebooks/david-copperfield.pdf'
    )
)

record_with_id = cid_client.create_cid(cid_input)
print(json.dumps(record_with_id, indent=2))

```


**CID Update**

```python
cid_input = UpdateCIDInput(
    cid='20.500.12592/zpc91w',
    who=PersonOrThingInput(
        thing=ThingInput(
            name='CID Client'
        )
    ),
    props=[PropertyValueInput(
        name='some property',
        value='some values'
    )],
    location=LocationInput(
        representation=[
            'https://www.gutenberg.org/files/6941/6941-h/images/titlepage.jpg',
            'https://www.gutenberg.org/files/6941/6941-h/images/dedication.jpg'
        ]
    )
)

record_with_id = cid_client.update_cid(cid_input)
print(json.dumps(record_with_id, indent=2))
```

**Assign Identifier**

```python
assign_parent_id = AssignIdentifierInput(
    cid='20.500.12592/34tmtg',
    identifier='20.500.12592/fj6qk0',
    type=IdentifierTypeInput.PARENT
)
updated_record = cid_client.assign_identifier(assign_parent_id)
print(json.dumps(updated_record, indent=2))
```

**Remove Identifier**

```python
remove_id_input = RemoveIdentifierInput(
    cid='20.500.12592/ncjthz',
    identifier='10.1037/arc0000014',
    type=IdentifierTypeInput.DOI
)

updated_record = cid_client.remove_identifier(remove_id_input)
print(json.dumps(updated_record, indent=2))
```

**Get by ID**

```python
cid = cid_client.get_by_id('20.500.12592/ncjthz')
```

**Get CID Children and Siblings**

```python
"""
    Find CID children and siblings.
    Returns list of matching CIDs and total.
    Result looks like this: {'total': 5, 'results': ['20.500.12592/ncjthz', ...]}
"""

search_res = cid_client.get_cid_children('20.500.12592/fj6qk0')
print(search_res)

search_res = cid_client.get_cid_siblings('20.500.12592/fj6qk0')
print(search_res)
```

**Get CID by artifact link**

```python
"""
    Find CID by artifact link.
    Returns list of matching CIDs and total. 
    Result looks like this: {'total': 5, 'results': ['20.500.12592/ncjthz']}
"""

search_res = cid_client.find_by_artifact("https://www.osha.gov/Publications/OSHA3990.pdf")
print(search_res)
```

## Extracting Artifact Full Text
If the artifact is text document (pdf, doc, ppt, rtf etc.) then you can request fulltext extraction.
Fulltext extraction is async. You can specify callback value to receive a notification by HTTP.

```python
extract_ft_input = ExtractFullTextInput(
    cid='20.500.12592/dev5tb369',
    callback=CallbackInput(
        url='https://example.com',
        method=HttpMethodInput.POST,
        params=[PropertyValueInput(
            name='foo',
            value='bar'
        )],
        headers=[PropertyValueInput(
            name='Content-Type',
            value='application/json'
        )]
    )
)
cid_client.extract_fulltext(extract_ft_input)
```

Code for retrieving values or checking if text is already extracted:
```python
cid_client.get_by_id('20.500.12592/dev5tb369', text_fields=['hasFullText'])

cid_client.get_by_id('20.500.12592/dev5tb369', text_fields=['rawText'])
```  

## Representation as IIIF format
You may notice that saved CID has a representation value like this: `https://images.coherentdigital.net/iiif/95x6mc/manifest.json`

This is universal format described here: [https://iiif.io/](https://iiif.io/).

IIIF format allows you to easily generate image galleries by various UI plugins like this: 
[http://universalviewer.io](http://universalviewer.io)


## Thumbnails

There is a simple rule one can generate a thumbnail for CID. See example:

[https://images.coherentdigital.net/ncjthz/300x300/thumbnail.png](https://images.coherentdigital.net/ncjthz/300x300/thumbnail.png)

So, the format is:

```
    https://images.coherentdigital.net/<CID_without_20.500.12592_fix>/<WIDTH>x<HEIGHT>/thumbnail.png
```
