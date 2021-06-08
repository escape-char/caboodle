import React from 'react';
import NotificationsIcon from '@material-ui/icons/Notifications';
import MoreIcon from '@material-ui/icons/More';
import {makeStyles} from '@material-ui/core/styles';
import {IconButton} from '../common/components/inputs'
import AccountCircle from '@material-ui/icons/AccountCircle';
import {Badge} from '../common/components/data';
import {ACCOUNT_MENU_ID, MOBILE_ACCOUNT_MENU_ID} from './constants';


const useStyles = makeStyles((theme)=>{
  return {
    sectionDesktop: {
      display: 'none',
      [theme.breakpoints.up('md')]: {
        display: 'flex',
      },
    },
    sectionMobile: {
      display: 'flex',
      [theme.breakpoints.up('md')]: {
        display: 'none',
      }
    }
  };
})

export default function AppBarActions() : React.ReactElement{
  const classes = useStyles();
  return (
    <>
      <div className={classes.sectionDesktop}>
        <IconButton aria-label="show 17 new notifications" color="inherit">
          <Badge badgeContent={17} color="secondary">
            <NotificationsIcon />
          </Badge>
        </IconButton>
        <IconButton
            edge="end"
            aria-label="account of current user"
            aria-controls={ACCOUNT_MENU_ID}
            aria-haspopup="true"
            color="inherit"
          >
            <AccountCircle />
          </IconButton>
      </div>
      <div className={classes.sectionMobile}>
          <IconButton
            aria-label="show more"
            aria-controls={MOBILE_ACCOUNT_MENU_ID}
            aria-haspopup="true"
            color="inherit"
          >
            <MoreIcon />
          </IconButton>
      </div>
    </>
  );
}
