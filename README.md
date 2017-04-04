# Insight Coding Challenge

## Structure

## Dependencies

This project uses Python 2.7. All modules used are part of the Python standard library: argparse, collections.Counter, csv, and datetime.

## Features

To facilitate feature development and abstract away the common operations for all features, I implemented a BaseFeature class. BaseFeature provides methods for reading text data, writing data back to a file, and extracting the top k elements from a collection. Since the output format is different for each feature, subclasses of BaseFeature implement a unique _data_to_string() method, which tells BaseFeature how to format the data it writes to the output file.

Since all features involve extracting columnar data from a text file, I implemented a module, read_server_log, to facilitate this. This module accepts a list of space-delimited strings and processes this data into types that Python can work with. This includes parsing the timestamp of the request into a datetime object.

Features are all called from process_log. All four features are isolated in try/except blocks, so failure of one feature will not affect the others. Errors are logged to a file, errors.txt.

### Feature 1

Feature 1 finds the most active hosts in the server log. To do this, we iterate over the rows in the log and keep track of the hit count for each host in a collections.Counter object mapping host -> hits. Then we can easily extract the top k hits from the Counter using heapsort, in O(n log k) time. Since scanning the log takes O(n) time, and our final sort takes O(n log k), that gives an overall performance of O(n log k).

Since we only use each row to update the Counter, there is no need to have the more than one row from the server log in memory at a time.

### Feature 2

The implementation of Feature 2 is similar to Feature 1. We iterate over the server log and keep track of the total bytes for each resource, again using a Counter object to map resource -> bytes. We again use Counter's heapsort to return the top k resources. As with Feature 1, we only need to hold a single line from the server log in memory at a time.

### Feature 3

In Feature 3, we are asked to find the busiest 60 minute window in the server log. The instructions note that a window need not begin with an event. However, the provided test case implies that the *first* window should begin with the first event, so I made that assumption.

e.g., in the test case, the log contains 10 events that occur between 00:00:01 and 00:00:15. In the test case, the expected answer has the busiest window beginning at 00:00:01, with 10 events. However, if we were to consider windows that begin *before* the first event, there would be many time windows encompassing all 10 events, e.g. 23:50:01, 23:50:02, 23:50:03, etc., on the previous day. However, given the expected output from the test case, I assume that we should not consider time windows that begin before the first logged event.

To solve this problem, I use a sliding window approach. I start with the first timestamp as my left bound, then slide my right bound out 60 minutes, keeping track of how many events I pass. I store the total number of events in this window in a Counter, mapping window start -> hits. Finally, I add one second to the left time bound (I assume second granularity for this problem) and update the left and right pointers accordingly.

This approach requires me to first scan all the timestamps into memory, requiring O(n) time and space. The runtime of the sliding window step depends both on the number of timestamps in the log (as our left and right pointers will scan over each element in the list once) and the difference between the first and last timestamps, in seconds (as our time bound will advance through all seconds in between). Therefore this approach is O(max(number of server logs, time between first and last server log in seconds)), which is linear.

### Feature 4

In Feature 4, we need to maintain block windows for hosts. Since these block windows may overlap in time (e.g. host A could be blocked at the same time as host B), I consider only one host at a time and scan ahead at fixed intervals. When I am finished scanning ahead for one host, I can move to the next host. Since this requires jumping forward and back in time, I cannot simply process the data one row at a time. Therefore I load the entire input into memory.

If it were not possible to load the full input into memory, I could first sort the data by both time and host, using an algorithm like MergeSort that can sort without having the entire data in memory at once. Then, I could iterate line-by-line, as each host can now be considered separately from others.
