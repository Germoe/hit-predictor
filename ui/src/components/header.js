import { Link } from "gatsby"
import PropTypes from "prop-types"
import React from "react"
import styled from "styled-components"
import mainImg from "../images/music_main_lg.jpg"

const HeaderStyle = styled.header`
  /*background-image: url("${mainImg}");
  background-position: center;
  background-size: cover;
  box-shadow: inset 0 0 500px black;*/
  background-color: #92319F;
  min-height: 400px;
  height: 40%;
  margin-bottom: 1.45rem;
`

const Header = ({ siteTitle }) => (
  <HeaderStyle>
    <div
      style={{
        margin: `0 auto`,
        maxWidth: 960,
        padding: `1.45rem 1.0875rem`,
      }}
    >
      <h1 style={{
        margin: 0,
        textAlign: `left`,
        margin: `50px 0 30px 0`,
        color: `white`,
        textDecoration: `none`
      }}>
        Hit Predictor
      </h1>
      <h4 style={{ textAlign: `left`, marginBottom: `100px` }}>
        <em>by Sebastian Engels</em>
      </h4>
    </div>
  </HeaderStyle>
)

Header.propTypes = {
  siteTitle: PropTypes.string,
}

Header.defaultProps = {
  siteTitle: ``,
}

export default Header
