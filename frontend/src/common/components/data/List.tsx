import React from 'react';
import {default as MList, ListProps as MListProps} from '@material-ui/core/List';

export type ListProps = MListProps;

export default function List(props:ListProps): React.ReactElement{
  return (<MList {...props}/>);
}
