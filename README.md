# Chess Game Backend API

## Overview
Welcome to the Chess Game Backend API Service. This is a Python Flask API application allows a client to make API calls to endpoints that:
* return a games current state
* save a games current state 
Further details about the applications JSON response, endpoints, dependencies, and other general configuration information can be found below. 

## Endpoints and JSON Contract
The Chess Game Backend API has x endpoints. 

### `Return a Games Current State by ID`
To have a specific games state returned  must hit the following API endpoint `/api/v1/games/:id?turn=turn_number`. T
