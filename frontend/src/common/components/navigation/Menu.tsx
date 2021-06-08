import React from 'react';
import {default as MMenu, MenuProps as MMenuProps} from '@material-ui/core/Menu';

export type MenuProps = MMenuProps;

export default function Menu(props: MenuProps){
  return (
    <MMenu {...props}/>
  );
}
