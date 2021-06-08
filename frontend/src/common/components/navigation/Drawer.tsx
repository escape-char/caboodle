import React from 'react';
import {default as MDrawer, DrawerProps as MDrawerProps} from '@material-ui/core/Drawer';

type DrawerProps = MDrawerProps;

export default function Drawer(props: DrawerProps): React.ReactElement{
  return (<MDrawer {...props}/>);
}
