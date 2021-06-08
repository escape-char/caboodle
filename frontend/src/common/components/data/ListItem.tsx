import React from 'react';
import {default as MListItem, ListItemProps as MListItemProps} from '@material-ui/core/ListItem'; 

export type ListItemProps = MListItemProps &  {button?: any; } ;

export default function ListItem(props: ListItemProps): React.ReactElement{
  return (<MListItem {...props}/>);
}
