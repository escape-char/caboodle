import React from 'react';
import {default as MAvatar, AvatarProps as MAvatarProps} from '@material-ui/core/Avatar';


export type AvatarProps = MAvatarProps;

export default function Avatar(props: AvatarProps):React.ReactElement{
  return (<MAvatar {...props}/>);
}
