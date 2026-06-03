# AI Lettings Enquiry Parser
### A lightweight Python application that uses an LLM to extract structured information from unstructured property enquiry emails.
## Features
### Extracts:
#### Enquirer name
#### Property reference
##### Enquiry type
##### Email address
##### Phone number
### Classifies enquiries as:
#### Viewing
#### Availability
#### General Question
### Flags missing information for manual review
### Outputs clean JSON suitable for CRM or database ingestion
## Installation
### Create a .env file:
### OPENAI_API_KEY=your_api_key_here
## Run
### python process_emails.py
### The script processes enquiry emails, validates extracted fields, and saves the results to output.json.
