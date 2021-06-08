import React from 'react';
import {default as MToolbar, ToolbarProps as MToolbarProps} from '@material-ui/core/Toolbar';

export type ToolbarProps = MToolbarProps;

export default function Toolbar(props:ToolbarProps){
  return <MToolbar {...props}/>
}
