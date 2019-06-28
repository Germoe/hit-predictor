import React from "react"
import { graphql } from "gatsby"
import Layout from "../components/layout"
import SEO from "../components/seo"
import styled from "styled-components"

const BlogContentStyled = styled.div`
  p {
    text-align: center;
  }

  a {
    color: #353535;
    text-decoration: none;
    border-bottom: solid #353535;
  }
`

export default function Template({
    data, // this prop will be injected by the GraphQL query below.
}) {
    const { markdownRemark } = data // data.markdownRemark holds our post data
    const { frontmatter, html } = markdownRemark
    return (
        <Layout>
            <SEO title="Report" />
            <div className="blog-post">
                <h1>{frontmatter.title}</h1>
                <BlogContentStyled
                    className="blog-post-content"
                    dangerouslySetInnerHTML={{ __html: html }}
                />
            </div>
        </Layout>
    )
}

export const pageQuery = graphql`
  query($path: String!) {
    markdownRemark(frontmatter: { path: { eq: $path } }) {
      html
      frontmatter {
        date(formatString: "MMMM DD, YYYY")
        path
        title
      }
    }
  }
`