import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import List, {ListProps} from '../common/components/data/List';
import {SIDEBAR_WIDTH} from './constants';

const defaultProps = {
  dense: true,
  disablePadding: true
}

const useStyles = makeStyles({
  'sidebarList': {
    width: `${SIDEBAR_WIDTH}px`
  }

});
function SidebarList(props: ListProps){
  const classes = useStyles();

  return (<List className={classes.sidebarList} {...props }/>);

}

SidebarList.defaultProps = defaultProps;
export default SidebarList;


