import React from 'react';
import {default as MHidden, HiddenProps as MHiddenProps} from '@material-ui/core/Hidden';

export type HiddenProps = MHiddenProps & {children: any};

export default function Hidden(props:HiddenProps):React.ReactElement{
  return (<MHidden {...props}/>);
}
