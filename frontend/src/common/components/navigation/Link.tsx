import React from 'react';
import {default as MLink, LinkProps as MLinkProps } from '@material-ui/core/Link';

export type LinkProps = MLinkProps;

export default function Link(props:LinkProps){
  return (<MLink {...props}/>);
}
