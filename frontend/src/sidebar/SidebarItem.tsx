import React from 'react';
import {ListItem, ListItemIcon, ListItemText} from '../common/components/data';
import {grey} from '@material-ui/core/colors';
import {makeStyles} from '@material-ui/core/styles';


const useStyles = makeStyles({
  itemCount:{
    float: "right",
    color: grey[500]
  },
  itemIcon:{
    minWidth: "36px"
  },
  itemTextIndent:{
    textIndent: "36px"
  }
});


type SideNavItemProps = {
  text: string,
  count?: number,
  iconComponent?: React.ReactNode

}

export default function SideNavItem(props: SideNavItemProps){
  const {text, count, iconComponent} = props;
  const classes = useStyles();

  return(
    <ListItem button>
      {iconComponent &&
        <ListItemIcon className={classes.itemIcon}>{iconComponent}</ListItemIcon>
      }
      <ListItemText className={iconComponent ? undefined : classes.itemTextIndent}>
        {text}
        {count &&
          <span className={classes.itemCount}>{count}</span>
        }
      </ListItemText>
    </ListItem>
  );
}
