# The Mail Service API

Reference: https://github.com/jenfi-eng/exam-long-mail-service


## Overview

### APIs

The app provides APIs for 3 main stakeholders:
- Post Master: mainly will fill the parcels into available trains and book the trains. Post Master will mainly uses below apis:
    - `GET /parcels`: to see all the parcels
    - `GET /trains`: to see all the available trains
    - `POST /parcels/fill`: to trigger the fullfilment operation, the system will automatically check for the available trains and fill the parcels in
    - `POST /trains/book`: to book the trains that already filled with parcels

- Train Operator: mainly manage the trains. Train Operator will main uses below apis:
    - `GET /trainlines`: to see all the operating train lines
    - `POST /trainlines`: to add a new train line
    - `GET /trains`: to see all the available trains
    - `POST /trains`: to add a new train
- Parcel Owner: these are our customers that will go to the system and book the parcel for shipping. Parcel Owner will primarily uses below apis:
    - `GET /parcels`: to see all the parcels
    - `POST /parcels`: to post a new parcel


### Business Flow

- The Train Operator will post the available trainlines and trains online for the Post Master to check which ones are available for shipping. The Train should have required information:
    - Weight: The total weight the train can carry
    - Volume: The total volume the train can carry
    - Cost: Cost of shipping

- The Parcel Owners will go to the system and post the parcels they want to ship. The parcel should have the required information:
    - Weight: the weight of the parcel
    - Volume: the volume of the parcel

- The Post Master then go to the system and see how many parcels are available for shipping. Then he/she can trigger the filling process to have the system assigns the approriate train for each parcel. After the filling process, the Post Master then can book the trains for shipping.


#### Filling process

The filling process will have two phases:
- Finding the trains that have the lowest costs and the total weight and total volume is equal or greater the total weight/volume of all the parcels.
- For each train, the system will then try to fill in the approriate parcels that can maximize the train capacity

#### Limitations
Due to time constraint, the app has some limitations as belows:

- Currently the system assumes the train weight/volume and the parcel weight/volume will have the same unit in integer, unit conversion was not implemented yet.
- Authentication / owenership is not implemented.
- Deletion / Withdrawal of parcels/trains is not impletemented yet
- Train line validation, checking for busyline is also not implemented yet. The system does not take into account the availability of train lines.
- The parcel filling operation currently only take into account the total weight of the train, more improvements need to be implemented to make sure the volume is fit

### How to start the app

#### Docker Compose
Simple run the command `docker compose up -d` to start the service with docker

#### Local Environment
- Require: Python 3.10
- Install all dependencies: `pip install -r requirements.txt`
- Start server with command: `uvicorn app.main:app`

#### Testing
- Install all test dependencies: `pip install -r requirements-dev.txt`
- Run test using pytest: `ENV_STATE=test pytest`

#### Swagger UI

You can check the API Specs and play around with the api using Swagger UI.
Simply opening any Browser and navigating to url: `http://localhost:8000/docs`



*Note: For simplicity, the app is using SQLite.