import React from 'react';
import {default as MListItemIcon, ListItemIconProps as MListItemIconProps} from '@material-ui/core/ListItemIcon';

export type ListItemIconProps = MListItemIconProps;

export default function ListItemIcon(props: ListItemIconProps): React.ReactElement{
  return (
    <MListItemIcon {...props} />
  );
}
