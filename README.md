# Readme

This branch contains the name level matching code.

## Approach

Since matching can be done for one collection across semesters, or
across multiple collections, input taken as two lists of field names.

Many of the fields may be common/same, these are matched together first.
Unmatched names are then chunked, and matched to get overall max similarity.

Chunks are based on entities from user stories, which are stored in a pickled trie.
To regenerate this dictionary, please run `python3 trie.py`. Prefix matching is done,
currently a minimum length >= 3 is needed to match.

## Output

(chunking is done; need to decide on chunk similarity metric)
(maybe identify future chunk candidates based on results from previous pass -- e.g. 'deptname' gets chunked as 'dept' + 'name' because
of 'department', so the chunk 'name' can be identified in other fields if similar naming conventions were followed)

```
Exact matches:
('exact', 1.0, 'fname', 'FName')
Remaining:
['lname', 'firstname']
['lastname', 'cameraMetadata']

Testing chunking...
['camera', 'metadata']
['dat', 'fromcam']
['username']
['dept', 'name']
['dep', 'artment']
['apartment']
['upload', 'dat', 'e']
['vehicle', 'description']
['vehicle', 'descript', 'on']

Matching: 'vehicleDescription' with 'vehicleDescripton'
vehicleDescription -> ['vehicle', 'description']
vehicleDescripton -> ['vehicle', 'descript', 'on']
('vehicle', 'vehicle')
('description', 'descript')
```
