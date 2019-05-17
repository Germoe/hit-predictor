Hit Predictor (Coming Soon - WIP)
==============================

This project uses Billboard Hot 100 and Spotify API data to make predictions on a song's potential to make it onto the Billboard Hot 100 (become a mainstream hit).

Quick Start
==============================

This project runs in an Anaconda Environment, I highly recommend running the following commands before you start:
1. `make create_environment` # This creates an Anaconda environment (you probably already have, but if not [install Anaconda](https://www.anaconda.com/distribution/))
2. `make data` # This pulls the necessary data files from an AWS S3 Bucket


Project Proposal
==============================

## What is the goal?

Everyday we hear songs played on the radio, curated by producers and created by artists and record labels. Most of these songs were judged on their catchiness and mass-appeal by experienced people before they made it onto the radio. Experience that can determine whether a song will be come a hit or not is a scarce resource. Which is why we'll look at the potential of a song to become a hit based on a song's features and the associated artist's clout.

Is it possible to tell from the song signature and additional meta data on the artist whether or not the song will become a hit and make it onto the Billboard Hot 100?

## Who cares?

Making it onto the Billboard Hot 100 is essential for most artists and record labels to make an income and to sustain their work. Understanding the potential for a song to make it onto the Billboard Hot 100 could be used as an additional input to inform the costly decision on whether or not a song should be put out as a single or get released at all.

We can even see a start-up dedicated to trying to simply solve this problem ([here](https://hyperlive.fm/)).
 
## What data are you going to use?

The data necessary to make this assessment are historic data which I'll acquire from the [Billboard Hot 100](https://www.billboard.com/charts/hot-100) and song- and artist-specific information, which I'll acquire from the Spotify API using the endpoints [/audio-analysis/](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/) and [/artists/](https://developer.spotify.com/documentation/web-api/reference/artists/get-artist/).

## What is your approach?

The definition of "Hit" for our purposes is limited to a song getting on the Billboard Hot 100.

To better understand the data sets, I'll explore the data Billboard Hot 100 set separately as well as combined with the audio features from the Spotify API.

The above analysis should yield a few possible candidates for features that can be used to predict the outcome of whether a song will make it onto the Billboard Hot 100.

To ensure that the possible features are valid, I'll formulate and test hypotheses for the data.

Once the features are created and chosen, I'll setup a supervised learning model to create the predictions.

## The Results

The code and documentation for this project will be available in this repository. Additionally, there'll be a Jupyter Notebook and an article. Depending on the success of the project, I'll create a website for other people to use the predictions engine and highlight the project.

---

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
