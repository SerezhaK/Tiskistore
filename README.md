# Store website with implementation of SMS registration via gateway sms.ru


### Before you install
Be sure you install the **submodule frontend**.  
You should clone the project using

    git clone -recurse-submodules …

or if you have already cloned the project, then use:

    git submodule update --init

___

### .env file setup

The .env file must be in the root directory

API_ID and LOGIN PASSWORD pair are mutually exclusive and need for gateway work.   
More detailed information can be found on the website sms.ru.

    DB_NAME=
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    DB_HOST=
    DB_PORT=
    
    SECRET_KEY=
    
    API_ID=
    SENDER=your-name
    TIMEOUT=900
    LOGIN=
    PASSWORD=
    
    DEBUG=1
    PHONE_NUMBER_CONFIRM=0
    
___

### Start project
Navigate to /infra/ 

    docker-compose up --build
