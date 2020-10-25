# VpnManager
### Django Rest Framework project

#### How to deploy
>OS: apt-based *[Ubuntu Server]*  
>Assuming python version >=3

Install necessary soft  
```
sudo apt-get -y install python-dev nginx python3-venv 
sudo pip install uwsgi
```

Then clone this repo into /opt/directory
```
git clone _this_repo_
```

Change dir to cloned repo. Create virtual environment and activate it.
```
cd /opt/_this_repo_
python -m venv venv
source venv/bin/activate
```
After that install `requirements.txt` via `pip`
```

pip install -r requirements.txt
```

So at this point our virtual environment is ready and all dependencies to run django app are acquired.  
First thing to do is creation of DB migration.
`VpnApp/seed/server_instance_seed.json` file contains sample models created.
```
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata VpnApp/seed/server_instance_seed.json
```

Don't forget about static assets from site-packages
```
python manage.py collectstatic
```

Create superuser
```
python manage.py createsuperuser
```

##### Nginx and uwsgi configuration

Now configure uwsgi.
Create directory `/etc/uwsgi/sites`
```
sudo mkdir /etc/uwsgi/sites
```


Move  `uwsgi.ini` file to `/etc/uwsgi/sites`
```
sudo mv uwsgi.ini /etc/uwsgi/sites
```
***!!! Modify `uwsgi.ini`  
Change `base = /opt/VpnManager` line according to project path located at your machine***


Create systemd upstart service:
```
sudo nano /etc/systemd/system/uwsgi.service
```
And paste this
```
[Unit]
Description=uWSGI Emperor service
After=syslog.target

[Service]
ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/sites
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```


Now configure nginx.
The nginx template file `VpnManger.nginx` should be moved to `/etc/nginx/sites-available` directory.  
Also create symlink to this file in `/etc/nginx/sites-enabled` directory.
```
sudo mv VpnManger.nginx /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/VpnManger.nginx /etc/nginx/sites-enabled/
```
***!!! Modify `VpnManger.nginx`  
Change `root = /opt/VpnManager` line according to project path located at your machine***

Run app
```
uwsgi 
sudo service nginx restart
```

----
### @Troubleshot
Project Directory should have `+rw` permission to write to database located in the same path as project  
Change ownership of database file `db.db` after migration to `www-data:www-data` 
