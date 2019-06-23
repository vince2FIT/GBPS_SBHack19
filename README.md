# GLOBAL BLOCKCHAIN PARCEL STANDARD (GBPS) - SBHACK19 - Intelligent Parcels

We are proud to introduce the *Global Blockchain Parcel Standard* as our submission for the Intelligent Parcels vertical in the Swiss Blockchain Hackathon 2019.

This README document serves three purposes:
1. Providing an overview of the basic idea of our system.
2. Serving as a set-up guide for our system as hosted on our Amazon EC2 resp. the documentation on the S3 bucket.
3. Giving a management summary for busy judges!

If you would like to inspect our hardware solution further, please feel free to call **+49 157 73847564**.

## Overview

### Our Hackathon Submission
The logistics of last-mile delivery increasingly poses challenges to its stakeholders. Customers requesting specific delivery times, congested cities and the resulting environmental issues, inefficient routes to remote areas and empty trips are just some of the examples.
An innovative solution to these challenges is to leverage other networks for last-mile transport, such as the mobility sharing economy, food delivery services, or - in the nearer futuer - autonomous machines.
However, this poses a variety of challenges as well. How do you integrate the individual networks transparently and efficiently? How do you handle permissions and traceability? And, first and foremost, how do you establish trust in the first place?

During the hackathon, we built an end-to-end system for the integration of external stakeholders for "hard-to-deliver" (e.g., too far off or too late) parcels on the last-mile. In particular, we enable parcel dispatchers (such as Die Post) to offer their unwanted parcel to other networks. Furthermore, the user of a ridesharing service (representing this other network) can then agree to deliver the parcel for cash. The necessary intermediary steps are implemented on a decentral blockchain layer, which has been created for the parcel logistics industry. This use case illustrates and technically builds on our broader vision (see below) perfectly, which is constituted by our **Global Blockchain Parcel Standard**.

In particular, we built the following components:

+ A web application with a multi-layer user interface for parcel dispatchers.
+ A (mobile) ridesharing web application with live maps, displaying the delivery jobs.
+ Several smart contracts connecting these two applications and providing logic.
+ A decentral private Ethereum logistics blockchain network hosting these smart contracts, which runs on an AWS EC2 instance.
+ As well as a functional hardware box with a self-built smart lock to illustrate further services and think the service end-to-end.
+ A n-node startup script for Quorum which unfortunately due to technical problems with the protocol we could not use for the final implementation of the case

### Why Blockchain?
Blockchain, or - more generally - distributed ledger technology is a vital component in our solution for one main reason: In the complex interorganizational processes in last mile parcel logistics, a jointly used platform can leverage an efficient flow of information and processes and drastically lower the number of needed standards and agreements. Instead of isolated data management and many bilateral contracts, there is one common platform resp. one agreed-on standard according to which all services are provided. Until shortly, such a platform on which adherence to specific rules hat to be ensured has not been possible without the service of a trusted, central intermediary. However, the leading companies in parcel logistics companies would not allow  a central intermediary to occupy a potential monopoly and thus potentially threatening both their business model because of the one-sided dependence. Otherwise, this would certainly already have been happened in such a highly competitive market.

Our blockchain network and the set of generic standard smart contracts deployed on it provide a neutral platform on which the described complex interorganizational processes in parcel logistics can be coordinated without the need for a central intermediary. Instead of the trusted intermediary, the cryptographic methods on which distributed ledger technology bases on and trust in the majority of the participants allow to enjoy all the advantages of a shared platform while avoiding the risk of a potentially monopolistic and costly intermediary. The major players such as big parcel delivery service providers run the platform jointly and at eye level, leveraging trust and transparency. The common standard and equality on the platform prevent lock-in effects, give access to the ecosystem also for smaller businesses and therefore make the market more effective and lift the to-date inefficiencies,  

Finally, a blockchain-based system is also well-suited for the challenges which IT-systems will face in the nearer future, such as integration of economically autonomous machines ("machine economy") and
It can also facilitate a more transparent data management, convincing consumers that their parcels are managed reliably and in the best possible way. For example, tracking services or machine-learning-based routing services can dock to the platform and offer their services to all of the participants.
With the help of advanced cryptographic methods such as Zero-Knowledge-Proofs and Secure Multiparty Computation, data privacy for both customers and businesses can be ensured and thus the perfect match between transparency and privacy can be achieved. Finally, our Blockchain facilitates carrying out microtransactions directly in the system, with small latencies and without transaction fees. 

### Our Vision
In the light of digitization, environmental exigencies as well as new modes of transport and changing customer requirements, the (parcel) logistics sector faces various challenges. While other sectors get disrupted one by one, the parcel logistics sector is still largely based on structures from decades ago. However, the new external demands require a parcel logistics solution fit for the 21st century.

The good news is, a wide variety of solutions for many of the challenges outlined before is already available. Companies such as *slock.it* create smart locks for enabling secure access to physical assets (such as parcels), start-ups like *modum.io* enable trustful tracking of critical transports and initiatives like *TradeLens* improve interorganizational shipping processes. The bad news is that these solutions are often based on isolated data silos, monopolist market structures, opacity, interorganizational process inefficiency and difficulties to enter markets sustainably. What is missing is a common infrastructure to connect all these brilliant individual solutions, enabling collaboration and efficient integration.

>We envision our **Global Blockchain Parcel Standard** to bridge the individual services and thereby create an innovative ecosystem for innovations in the parcel logistics sector. A first step has already been presented with our smart contract standards, smart lock hardware solution and the creation of our private Quorum logistics blockchain in the Hackathon.

## Set-up Guide
To test our system, you require nothing more than a web browser and some curiosity.

1. Blockchain and so on?
2. Front-End for dispatcher
3. Front-End for sharer

This is the URL to our working solution:

`S3-URL`

Of course, if you are interested in the technical details, we would love to see you around our GitHub repository. You can find our code under the following URL:

`https://github.com/vince2FIT/GBPS_SBHack19`

The repository should be fairly self-explanatory, but here are some hints nevertheless:
Our web application for parcel dispatchers is built as an Angular project. The main scripts are XX.

## Key Take-Aways
+ During the hackathon, we built a decentral and open end-to-end system for the integration of non-logistics networks into parcel logistics use cases, such as delivering "hard-to-deliver" parcels on the last-mile.
+ Our vision is that our **Global Blockchain Parcel Standard** bridges individual services related (but not limited) to parcel logistics and thereby creates an innovative ecosystem for innovations in this and other sectors.
+ Link to our working application: `S3-URL`
+ Link to our GitHub repository: `https://github.com/vince2FIT/GBPS_SBHack19`
