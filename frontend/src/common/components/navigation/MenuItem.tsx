import React from 'react';
import {default as MMenuItem, MenuItemProps as MMenuItemProps} from '@material-ui/core/MenuItem';

export type MenuItemProps = MMenuItemProps & {button: any};

export default function MenuItem(props: MenuItemProps){
  return (<MMenuItem {...props}/>);
}
