import React from '@material-ui/core/Badge';
import {default as MBadge, BadgeProps as MBadgeProps} from '@material-ui/core/Badge';

export type BadgeProps = MBadgeProps;

export default function Badge(props:BadgeProps): React.ReactElement{
  return (<MBadge {...props}/>);
}
