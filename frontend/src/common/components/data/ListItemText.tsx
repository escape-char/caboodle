import React from 'react';
import {default as MListItemText, ListItemTextProps as MListItemTextProps} from '@material-ui/core/ListItemText';

type ListItemTextProps = MListItemTextProps;

export default function ListItemText(props: ListItemTextProps){
  return (
    <MListItemText {...props} />
  );
}
