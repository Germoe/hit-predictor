# Data

The heart of this project is as with any Data Science project _the Data_. The data for this project due to its size lives in an AWS S3 Bucket.

There are 2 ways to get the data:
- Download the directory from `s3://hit-predictor/data/` and store its contents in the respective directory inside `./data/`. 
- Alternatively, download all the data by running `make data` in the cloned repository and activated environment
