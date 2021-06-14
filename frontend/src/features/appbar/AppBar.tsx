import React from 'react';
import {makeStyles } from '@material-ui/core/styles';
import MenuIcon from '@material-ui/icons/Menu';
import AppBar, {AppBarProps as MAppBarProps} from '../../common/components/bars/AppBar';
import {IconButton} from '../../common/components/inputs';
import Toolbar from '../../common/components/bars/Toolbar';
import AppBarHeader from './AppBarHeader';
import AppBarActions from './AppBarActions';
import {InputSearch} from '../../common/components/inputs';
import { APP_BAR_HEIGHT } from '../../common/theme';

export type AppBarProps = MAppBarProps & {
  header: string,
};

const defaultProps = {position:"sticky"};


const useStyles = makeStyles((theme) => ({
  menuButton: {
    marginRight: theme.spacing(2),
  },
  grow: {
    flexGrow: 1,
  },
  toolbar:{
    minHeight: `${APP_BAR_HEIGHT}px`
  }
}));

function CAppBar(props:AppBarProps){

  const classes = useStyles();

  return (
    <AppBar>
      <Toolbar className={classes.toolbar}>
        <IconButton
            edge="start"
            className={classes.menuButton}
            color="inherit"
            aria-label="open drawer"
          >
            <MenuIcon />
        </IconButton>
        <AppBarHeader header={props.header}/>
        <div className={classes.grow} />
        <InputSearch/>
        <AppBarActions/>
      </Toolbar>
    </AppBar>
  );
}

CAppBar.defaultProps = defaultProps;
export default CAppBar;


