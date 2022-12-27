## MultiThreading

### Quick Look
- Consumer-Producer
- Queue

### Aim
With this code we simulate a multi-threaded program. 
The program aims to understand how many times a company is mentioned in social media and whether it is positive or negative.

### Summary

There is a Producer-Consumer structure in which the Producer is called Collector which collects tweets from social media and then sends them to the Queue.
The Consumer is called Analyzer which reads tweets from the queue and increments the sentiment counters accordingly.
