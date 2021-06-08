import React from 'react';
import {default as MGrid, GridProps as MGridProps} from '@material-ui/core/Grid';

export type GridProps = MGridProps

export default function Grid(props: GridProps):React.ReactElement{
  return <MGrid {...props}/>
}
