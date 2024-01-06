# Store website with implementation of SMS registration via gateway sms.ru


#### Before use, make sure that you have **submodule frontend** installed
You should clone the project using

    git clone -recurse-submodules …

or if you have already cloned the project, then use:

    git submodule update --init

### Start project
Navigate to /infra/ 

    docker-compose up --build

### .env file

The .env file must be in the root directory

API_ID and LOGIN PASSWORD pair are mutually exclusive and need for gateway work 
More detailed information can be found on the website sms.ru.

    DB_NAME=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    DB_HOST=db
    DB_PORT=
    
    SECRET_KEY=

    API_ID=
    LOGIN=
    PASSWORD=
    
    DEBUG=
    PHONE_NUMBER_CONFIRM=