import React, { Component } from "react"
import { graphql } from "gatsby"
import axios from "axios"
import styled, { createGlobalStyle } from "styled-components"
import AWS from "aws-sdk"
import Header from "../components/header"

const GlobalStyles = createGlobalStyle`
  body {
    @import url('https://fonts.googleapis.com/css?family=Roboto');
    font-family: 'Roboto', sans-serif;
  }
`

// This query is executed at build time by Gatsby.
// export const GatsbyQuery = graphql`
//   {
// rickAndMorty {
// character(id: 1) {
// name
// image
//       }
//     }
//   }
// `

const SearchContainerStyle = styled.div`
  width: 100%; 
  text-align: center;
  padding: 20px 10% 10% 10%;
`

const SearchInputStyle = styled.input`
  min-width: 300px;
  height: 60px;
  padding: 0 100px;
  margin: 10px 30px;
  border-radius: 50px;

  :focus {
    outline: none;
  }
`

const SearchButtonStyle = styled.button`
  border-color: #92319F;
  width: 200px;
  height: 60px;
  padding: 0 10px;
  margin: 10px 30px;
  border-radius: 50px;

  :hover, :focus {
    outline: none;
    background-color: #92319F;
    color: #FFFFFF;
  }
`

const ButtonStyle = styled.button`
  border-color: #92319F;
  width: 200px;
  height: 40px;
  padding: 0 10px;
  margin: 10px 30px;
  border-radius: 50px;

  :hover, :focus {
    outline: none;
    background-color: #92319F;
    color: #FFFFFF;
  }
`

const ListStyle = styled.div`
  width: 95%;
  max-width: 600px;
  margin: 50px auto auto auto;
`

const SongContainerStyle = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  text-align: center;
`

const AlbumImageContainerStyle = styled.div`
  width: 30%;
`

const TextContainerStyle = styled.div`
  width: 70%;
`


AWS.config.update({ region: 'us-east-2' });
AWS.config.credentials = new AWS.CognitoIdentityCredentials({ IdentityPoolId: 'us-east-2:28d93f6b-36ae-4739-afff-c7739b0a345e' });

const Button = ({ loading, text, func }) => (
  <>
    {loading ? <ButtonStyle>Calculating ...</ButtonStyle> : <ButtonStyle onClick={func}>{text}</ButtonStyle>}
  </>
)

class Predict extends Component {
  state = {
    loading: false,
    hasPrediction: false,
    prediction: {},
    features: []
  }

  render() {
    return (
      <div>
        {this.state.hasPrediction ? <p>{this.state.prediction.hit ? 'Hit' : 'No Hit'}
          <br />
          Certainty: {Math.round(this.state.prediction.certainty * 10000) / 100}%
        </p> : <Button loading={this.state.loading} text="Get Prediction" func={this.getPrediction} />}
      </div>
    )
  }

  getPrediction = () => {
    this.setState({ loading: true })
    const sp = axios.create({
      baseURL: 'https://api.spotify.com/v1/',
      headers: {
        'Authorization': 'Bearer ' + this.props.access_token,
        'content-type': 'application/json'
      }
    })
    sp
      .get(`/audio-features/${this.props.data.id}`)
      .then(res => {
        const { data } = res
        const feature_names = ['acousticness', 'loudness', 'instrumentalness', 'danceability', 'valence', 'energy', 'duration_ms']
        let features = []
        feature_names.map(name => {
          features.push(data[name])
        })
        this.scoreFeatures([features])
      })
      .catch(err => {
        this.setState({ loading: false, err })
      })
  }

  scoreFeatures = features_list => {
    var lambda = new AWS.Lambda({ region: 'us-east-2' });
    if (features_list.length == 0) {
      prompt('Not Enough Features Found. Try and refresh!')
      return
    }

    const payload = {
      features: features_list
    }

    // create JSON object for parameters for invoking Lambda function
    var pullParams = {
      FunctionName: 'hit_predictor_score',
      InvocationType: 'RequestResponse',
      LogType: 'None',
      Payload: JSON.stringify(payload)
    };
    // create variable to hold data returned by the Lambda function
    var pullResults;
    lambda.invoke(pullParams, function (error, data) {
      if (error) {
        console.log(error);
      } else {
        pullResults = JSON.parse(data.Payload);
        const onePrediction = pullResults['values'][0]
        this.setState({
          loading: false,
          hasPrediction: true,
          prediction: {
            hit: onePrediction[0],
            certainty: onePrediction[1][onePrediction[0]]
          }
        })
      }
    }.bind(this));
  }
}

const Song = ({ data, access_token }) => (
  <SongContainerStyle>
    <AlbumImageContainerStyle>
      <img src={data.album.images[1].url} />
    </AlbumImageContainerStyle>
    <TextContainerStyle>
      <p>{data.name}</p>
      <Predict data={data} access_token={access_token} />
    </TextContainerStyle>
  </SongContainerStyle >
)

class Main extends Component {
  state = {
    loading: false,
    q: 'Michael Jackson',
    error: false,
    token: false,
  }

  componentDidMount() {
    console.log('mount')
    console.log(this.state.token)
    if (this.state.token == false) {
      console.log('setting token')
      this.setToken()
    }
  }

  setToken = () => {
    var lambda = new AWS.Lambda({ region: 'us-east-2' });
    // create JSON object for parameters for invoking Lambda function
    var pullParams = {
      FunctionName: 'hit_predictor_sp_client_token',
      InvocationType: 'RequestResponse',
      LogType: 'None'
    };
    // create variable to hold data returned by the Lambda function
    var pullResults;
    lambda.invoke(pullParams, function (error, data) {
      if (error) {
        console.log(error);
      } else {
        pullResults = JSON.parse(data.Payload);
        this.setState({ token: pullResults })
      }
    }.bind(this));
  }

  render() {
    const items = this.state.items
    return (
      <>
        <Header siteTitle="Predictions" />
        <SearchContainerStyle>
          <GlobalStyles />
          <SearchInputStyle value={this.state.q} onChange={this.handleChange} />
          <SearchButtonStyle onClick={this.fetchSpotifyCredentials}>Search</SearchButtonStyle>
          <ListStyle>{this.state.loading ? (
            <p>Loading Songs</p>
          ) : items ? (
            items.map(data => <Song key={data.id} data={data} access_token={this.state.token.access_token} />)
          ) : null}
          </ListStyle>
        </SearchContainerStyle>
      </>
    )
  }

  handleSubmit = (e) => {
    console.log(e.target)
  }

  handleChange = (e) => {
    const input_val = e.target.value
    this.setState({
      q: input_val
    })
  }

  fetchSpotifyCredentials = () => {
    console.log(this.state.token)
    this.setState({ loading: true })
    const sp = axios.create({
      baseURL: 'https://api.spotify.com/v1/',
      headers: {
        'Authorization': 'Bearer ' + this.state.token.access_token,
        'content-type': 'application/json'
      }
    })
    sp
      .get(`/search?q=${this.state.q}&type=track`)
      .then(res => {
        const { data: { tracks: { items } } } = res
        this.setState({
          loading: false,
          items: items
        })
      })
  }

  fetchRicksPupper = () => {
    this.setState({ loading: true })
    const instance = axios.create({
      baseURL: 'https://dog.ceo/api/breeds/image/'
    })
    instance
      .get(`/random`)
      .then(pupper => {
        const {
          data: { message: img },
        } = pupper
        const breed = img.split("/")[4]
        this.setState({
          loading: false,
          pupper: {
            ...this.state.pupper,
            img,
            breed,
          },
        })
      })
      .catch(error => {
        this.setState({ loading: false, error })
      })
  }
}

export default Main