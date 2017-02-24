Mobiventory
====================
A thesis project

## Requirements
  1. `git`
  1. `python3.5` or higher
  1. `virtualenv`

## Source code replication

  1. Go to repository [homepage](https://github.com/LordSalfo/mobiventory)
  
  1. Click `Clone or download` green button on the right side
  
  1. Click `Use HTTPS`
  
  1. Copy given link
  
  1. Go to your terminal/cmd
  
  1. Create your virtualenv(given that you have python3.5 installed):
  
    `virtualenv -p python3.5 env`
  
  1. Go to your terminal and type:
 
    `git clone https://github.com/LordSalfo/mobiventory`
  
  1. **Activate your virtualenv**
  
    *WINDOWS*:
    
      `env/bin/activate`
      
    *LINUX*:
    
      `. env/bin/activate`
      
  1. Go to project and install requirements
  
    ```shell
    cd mobiventory
    pip install -r requirements.txt
    ```
    
  1. Run application
  
    `./manage.py runserver 0:8000`
  
## Creating superuser
  
  1. Execute command and fill up details(the email is optional):
  
    `./manage.py createsuperuser`
