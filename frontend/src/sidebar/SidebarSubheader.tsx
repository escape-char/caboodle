import React from 'react';
import ListSubheader from '@material-ui/core/ListSubheader';
import {ListItem} from '../common/components/data';

export type SidebarSubheaderProps = {text: string};

export default function SidebarSubheader(props: SidebarSubheaderProps){
  const {text} = props;
  return (
    <ListItem>
      <ListSubheader>{text}</ListSubheader>
    </ListItem>
  );
}


