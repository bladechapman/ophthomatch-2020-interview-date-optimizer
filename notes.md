### Network Notes

Edge column going from source to every school node
- capacity 1
- unit cost 0

Edge column going from every date to terminal node
- capacity 1
- unit cost 0


Edge column going from every school to every date that school offers
- capacity 1
- unit cost = school rank


Source node has unit supply=20


### Programming notes
- map every school to a node index
- map every date to a node index
- create an index for source
- create an index for sink

1. construct source-to-school edges
- iterate over schools
- append columns for each school

2. construct date-to-sink edges
- iterate over dates
- append columns for each date

3. construct school-to-date edges
- iterate over dates per school
- if cell has value 1 for a date, look up date index, create column with capacity of rank
