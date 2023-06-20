# QAware Code Night @ Schloss Gymnasium Mainz

Repository to store code, which is used at the Code Night at the "Gymnasium am Kurfürstlichen Schloss Mainz".

## Installation

1.) Install all dependencies:

```
pip install -r requirements.txt
```

2.) Start the database:

```
docker compose up -d
```

3.) Start the uvicorn backend:

```
uvicorn main:app --reload
```

The reload command is used to be able to update the code and start the application automatically.

## Usage

After the installation the API can be called via curl or the browser to serve the user with data or as data storage.

## Maintaner

R. Kalleicher, <robin.kalleicher@qaware.de>     
C. Thelen, <christoph.thelen@qaware.de>
