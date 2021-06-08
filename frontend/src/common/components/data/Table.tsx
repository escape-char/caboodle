import React from 'react';
import {default as MTable, TableProps as MTableProps} from '@material-ui/core/Table';

export type TableProps = MTableProps;

export default function Table(props: TableProps): React.ReactElement{
  return (<MTable {...props} />);
}
