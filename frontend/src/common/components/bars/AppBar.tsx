import React from 'react';
import {default as MAppBar, AppBarProps as MAppBarProps} from '@material-ui/core/AppBar';

export type  AppBarProps = MAppBarProps;

export default function AppBar(props: AppBarProps) {
  return (
    <MAppBar {...props} />
  );
}
