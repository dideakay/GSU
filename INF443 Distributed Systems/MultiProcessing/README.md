## MultiProcessing With Queue

### Quick Look
- Consumer-Producer
- Queue
- Process Communication

### Aim
With this code we simulate a multi-processing program. The program aims to understand how many times a company is mentioned in social media.

### Summary


There is a Producer-Consumer structure in which the Producer is called Collector which collects tweets from social media and then sends them to the Queue. The Consumer is called Analyzer which reads tweets from the queue and increments the sentiment counters accordingly.

Noticed that at the beginning 10 collector instances are created and only 3 analyzer instances are created. In this case the collectors are creating more data than the analyzers can read.  That's why a queue structure is suitable for the communication between processes.

Also in order to allow child and parent processes to have common variables that they can both see and modify, Value class is used from the multiprocessing library.
