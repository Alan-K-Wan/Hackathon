# Hackathon 

## Team 
- Alan 
- Brandon 
- Geemal 
- Georgia 
- Kelvin 

## Client 
Shane – Wesfarmers Chemicals, Energy, and Fertilisers (WESCEF) 

## Problem Statement 
Traditional service desk ticketing systems are often slow and inconvenient for both client and IT technicians. Sometimes basic requests such as resetting a password takes days to complete! This is due to several factors including: 
- Clients cannot get help of business hours. 
- Long delays in response from both parties. 
- Unclear or lack of information to complete a request. 
- Approval is required before service can be completed. 
In addition, these inefficiencies prevent IT technicians from completing more complex requests in a timely manner. They often find themselves bogged down by the sheer volume of routine and time-consuming tasks. 

## Proposed Solution 
WESCEF wants to create a an intelligent chatbot for the service desk analysts that allows the user to query the knowledge bases and identify self-help mechanisms. The chatbot is to be called “Ask WESly” and have the following features: 
- An application for clients to conveniently request a service^ and instantly receive a response. A response may be a link to a self-help article or further questions if not enough information was provided.  
- A portal for IT technicians in which requests are automatically classified into priority. 
- If the chatbot is unable to fulfil the clients request, then the ticket is escalated to a real person.   
- The chatbot should automatically email authorised individuals for tickets that require approval for example loaning hardware.

## Approach 
- Use Django to quickly whip up a user interface and backend including authentication 
- Use OpenAI API calls to provide responses to clients
  - Have a database of types of requests and information required for such request 
  - keep asking the client questions until all the information has been received
- Use GitHub copilot to code some algorithms which email people based on what needs approval 
- Add appropriate music when question is asked. This will sooth clients’ thought process 
- Most importantly, create a presentation that makes our solution look very good even if it’s not that great 

## Specification 
The product will be composed of three main components. 
1. Prompt engine 
- Responsible for returning a response to the user that is understandable, professional, and friendly. 
- Asks the user for specific information if required 
- Translate technical terminology into layman's terms 
- Engage in relevant conversations 
2. Logic processor 
- Analyses the request and identifies the information required to complete the request 
- Keeps track of information that the customer has already provided 
- Links information collected to a database or specific article if it has high confidence 
3. Data relay service 
- Augments information gathered by the logic processor into technical language model for service desk specialist 
- Open communication channel between client and specialist 

## Footnotes
^ a service may be hardware request, installing software on a computer, troubleshooting software or hardware issues, request access to a resource, etc. 
