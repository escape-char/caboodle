import React from 'react';
import {default as MChip, ChipProps as MChipProps} from '@material-ui/core/Chip';

export type ChipProps = MChipProps;

export default function Chip(props:ChipProps): React.ReactElement{
  return (<MChip {...props}/>);
}
