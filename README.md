EtherPool Stats
---

* no longer works due to cloudflare DDOS protection *
* cloudscrape partially fixed this issue, but cuts off after 50 requests from the same IP *


### Purpose:

**example output**

* *The* **blue** *line is the amount of ether mined* 

* *the* **orange** *line is mining speed in MH/s (mega-hashes per second) reported by the pool*

![alt text]
(http://i.imgur.com/ziXGSQT.png =700x350 "Logo Title Text 1")


This app is built on top of two modest python scripts and api integration with Plotly for streaming charts.

In short this app was just meant to record the pool-reported hash-rate and current share-value of my ethereum miner as it was mining on EthPool.

Early on, the algorythym EthPool (an ethereum mining pool) used to define shares within a given time-window was odd, in that shares seemed to decrease inbetween found blocks, the reported hash-rate was also all over the place, so I decided to create a small database driven tool to track these metrics.

### Conclusion:

I initially was only mining ethereum due to my involvement in the project from the early days of the test-net and because I wanted some ether to use for testing my own smart-contracts.  As of now, mining ethereum even with two or three relatively high-performance AMD GPU's isn't worth it anymore, at this point I'd be lucky to get 1.5 Eth per day even when mining with a mining pool.  Not to mention the fact that ethpool's website prevents this script from properly polling metrics anymore.

I do plan to stay involved with the ethereum project and think it has lots of promise to become one of the premiere blockchain technologies of the future.
