Hit Predictor
==============================

This project uses Billboard Hot 100 and Spotify API data to make predictions on a song's potential to make it onto the Billboard Hot 100 (become a mainstream hit).

Quick Start
==============================

This project runs in an Anaconda Environment, I highly recommend running the following commands before you start:
1. `git clone https://github.com/Germoe/hit-predictor.git && cd hit-predictor` # Clone Repository and Navigate to Directory
2. `make environment` # This creates an Anaconda environment (you probably already have it installed, but if not [install Anaconda](https://www.anaconda.com/distribution/))
3. `conda activate hit-predictor` # Activate the Environment
4a. `make data` # This pulls the necessary data files from an AWS S3 Bucket
4b. If you plan on generating data or deploying models yourself make sure to generate a `.env` file based on the `env` template file.

Directory Structure
==============================

- **Data**: This is where all of the Data lives (has to be downloaded from an S3 bucket or generated using the application in `src`)
- **Models**: The Models and Pipelines are stored in this directory.
- **Notebooks**: This directory includes the Notebooks and Code for the main part of the data wrangling, exploration and model generating (This is likely the most interesting directory to explore if you're interested in how everything comes together)
- **References**: This directory is empty as most of the references that were used are proprietary and I'm unable to provide these references as a full version. If you're interested in the references feel free to reach out to me at [me@sebastian-engels.com](mailto:me@sebastian-engels.com)
- **Reports**: This is where you should start. It includes the project report and slides to get an overview what this project tackles.
- **src**: This is the main code base that was used to sample, scrape and generate the data
- **ui**: This directory holds the frontend interface that is deployed at [hit-predictor.com](https://www.hit-predictor.com) 

Project Proposal
==============================

## What is the goal?

Everyday we hear songs played on the radio, curated by producers and created by artists and record labels. Most of these songs were judged on their catchiness and mass-appeal by experienced people before they made it onto the radio. Experience that can determine whether a song will be come a hit or not is a scarce resource. Which is why we'll look at the potential of a song to become a hit based on a song's features and the associated artist's clout.

Is it possible to tell from the song signature and additional meta data on the artist whether or not the song will become a hit and make it onto the Billboard Hot 100?

## Who cares?

Making it onto the Billboard Hot 100 is essential for most artists and record labels to make an income and to sustain their work. Understanding the potential for a song to make it onto the Billboard Hot 100 could be used as an additional input to inform the costly decision on whether or not a song should be put out as a single or get released at all.

We can even see a start-up dedicated to trying to solve this problem ([here](https://hyperlive.fm/)).
 
## What data are you going to use?

The data necessary to make this assessment are historic data which I'll acquire from the [Billboard Hot 100](https://www.billboard.com/charts/hot-100) and song-specific information, which I'll acquire from the Spotify API using the endpoints [/get-audio-features/](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/).

## What is your approach?

The definition of "Hit" for our purposes is limited to a song getting on the Billboard Hot 100.

To better understand the data sets, I'll explore the data Billboard Hot 100 set separately as well as combined with the audio features from the Spotify API.

The above analysis should yield a few possible candidates for features that can be used to predict the outcome of whether a song will make it onto the Billboard Hot 100.

To ensure that the possible features are valid, I'll formulate and test hypotheses for the data.

Once the features are created and chosen, I'll setup a supervised learning model to create the predictions.

## The Results

The code, notebooks and documentation for this project can be found in this repository. Additionally, slides and a project report can be found in the `reports` directory. Lastly, you can try out the model by using the web app at [hit-predictor.com](https://hit-predictor.com).

---

#### Found any issues?

If you saw any typos or issues (methodology or code), I'd be very happy if you could open an issue on this repository. If you'd like to connect and exchange ideas feel free to send me an e-mail [me@sebastian-engels.com](mailto:me@sebastian-engels.com) or reach out on [LinkedIn](https://www.linkedin.com/in/sebastianengels/) and make sure to reference this project.

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
