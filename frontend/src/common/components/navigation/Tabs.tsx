import React from 'react';
import {default as MTabs, TabsProps as MTabsProps} from '@material-ui/core/Tabs';

export type TabsProps = MTabsProps;

export default function Tabs(props: TabsProps){
  return (<MTabs {...props}/>);
}
