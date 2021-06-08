import React from 'react';
import {default as MIconButton, IconButtonProps as MIconButtonProps} from '@material-ui/core/IconButton';


type IconButtonProps = MIconButtonProps;

export default function IconButton(props: IconButtonProps){
  return (<MIconButton {...props}/>);
}
