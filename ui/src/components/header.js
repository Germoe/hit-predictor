import { Link } from "gatsby"
import PropTypes from "prop-types"
import React from "react"
import styled from "styled-components"
import mainImg from "../images/music_main_lg.jpg"

const HeaderStyle = styled.header`
  /*background-image: url("${mainImg}");
  background-position: center;
  background-size: cover;
  box-shadow: inset 0 0 500px #F46425;*/
  background-color: #F46425;
  color: #FFFFFF;
  text-shadow: 2px 2px #353535;
`

const NavStyle = styled.div`
  background-color: #353535;
  width: 100%;
  min-height: 60px;
  box-shadow: -5px 5px 5px #a3a3a3;
  border-top-style: solid;
  border-top-width: 1px;
  border-top-color: #FFFFFF;
  margin-bottom: 1.45rem;

  & > div {
    display: flex;
    flex-direction: row;
    width: 200px;
    margin-left: auto;
    margin-right: auto;
    justify-content: space-between;
    line-height: 60px;
  }
`

const Header = ({ siteTitle }) => (
  <>
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
          margin: `50px 0 15px 0`,
          textDecoration: null
        }}>
          Hit Predictor
      </h1>
        <h4 style={{
          textAlign: `left`,
          marginBottom: `50px`
        }}>
          <em>by Sebastian Engels</em>
        </h4>
      </div>
    </HeaderStyle>
    <NavStyle>
      <div>
        <div><Link to="/"
          style={{
            color: "#FFFFFF",
            textDecoration: 'none',
          }}
          activeStyle={{ borderBottom: "solid #FFFFFF" }}
        ><strong>Predictor</strong></Link></div>
        <div><Link to="/report"
          style={{
            color: "#FFFFFF",
            textDecoration: 'none',
          }}
          activeStyle={{ borderBottom: "solid #FFFFFF" }}
        ><strong>Report</strong></Link></div>
      </div>
    </NavStyle>
  </>
)

Header.propTypes = {
  siteTitle: PropTypes.string,
}

Header.defaultProps = {
  siteTitle: ``,
}

export default Header
