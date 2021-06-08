import React from 'react';
import {default as MBreadcrumbs, BreadcrumbsProps as MBreadcrumbsProps} from '@material-ui/core/Breadcrumbs';

export type BreadcrumbsProps = MBreadcrumbsProps;

export default function Breadcrumbs(props:BreadcrumbsProps){
  return (<MBreadcrumbs {...props}/>);
}
