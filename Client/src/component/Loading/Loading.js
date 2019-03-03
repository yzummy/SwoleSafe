import React from 'react';
import { css } from '@emotion/core';

import RiseLoader from 'react-spinners/RiseLoader';
 
// const override = css`
//     display: block;
//     margin: 0 auto;
//     border-color: red;
// `;
 
const override = {
    display: 'block',
    margin: '0 auto',
    // border-color: 'red'
 };

class Loading extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    //   loading: true
    }
  }
  render() {
    return (
      <div className='sweet-loading'>
        <RiseLoader
          style={override}
          sizeUnit={"px"}
          size={15}
          color={'#123abc'}
          loading={this.props.loading}
        />
      </div> 
    )
  }
}

export default Loading;