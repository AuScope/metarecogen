### NOTES for building & running 'ckan_to_gn.py' as a standalone docker image

* Build
```
sudo docker build -t ckan2gn .
```

* Create .env file with 'CKAN2GN_CKAN_URL' 'CKAN2GN_GN_PASSWORD' 'CKAN2GN_GN_URL' 'CKAN2GN_GN_USERNAME' defined e.g.
```
CKAN2GN_CKAN_URL=https://myckan
CKAN2GN_GN_PASSWORD=secretblah
CKAN2GN_GN_URL=https://mygeonetwork
CKAN2GN_GN_USERNAME=username
```

* Run
```
sudo docker run --env-file .env --network host ckan2gn
```
