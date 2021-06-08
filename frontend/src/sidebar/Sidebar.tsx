import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import {grey} from '@material-ui/core/colors';
import Divider from '@material-ui/core/Divider';
import ListItemSubheader from '@material-ui/core/ListSubheader';
import LanguageIcon from '@material-ui/icons/Language';
import BookmarksIcon from '@material-ui/icons/Bookmarks';
import SortIcon from '@material-ui/icons/Sort';
import DraftsIcon from '@material-ui/icons/Drafts';
import FavoriteIcon from '@material-ui/icons/Favorite';
import {Hidden} from '../common/components/layouts';
import {Drawer} from '../common/components/navigation';
import {List, ListItem, ListItemText, ListItemIcon} from '../common/components/data';
import {APP_BAR_HEIGHT} from '../common/theme';
import SidebarItem from './SidebarItem';
import SidebarList from './SidebarList';
import SidebarSubheader from './SidebarSubheader';


const DRAWER_WIDTH="240px";
const useStyles = makeStyles((theme)=>{
  return {
    sidebar: {
      background: theme.palette.primary.main,
      [theme.breakpoints.up('sm')]: {
        width: DRAWER_WIDTH,
        flexShrink: 0,
      },
    },
    paper: {
      height:`100% - ${APP_BAR_HEIGHT}`,
      background: grey[200],
      top: APP_BAR_HEIGHT
    },
    drawer:{
      width: DRAWER_WIDTH
    },
    toolbar: theme.mixins.toolbar
  };
})


export default function Sidebar(){
  const container = window !== undefined ? () => window.document.body : undefined;
  const classes = useStyles();

  return(
    <nav className={classes.sidebar} aria-label="sidebar navigation">
      <Hidden xsDown implementation="css">
        <Drawer 
          className={classes.drawer}
          variant="permanent"
          PaperProps={{className:classes.paper}}
          open
        >
          <div>
              <SidebarList>
                <SidebarItem text="Browse" iconComponent={<LanguageIcon/>}/>
              </SidebarList>
              <Divider/>
            <div className={classes.toolbar}>
              <List className={classes.drawer} disablePadding dense>
                <SidebarSubheader text="My Bookmarks"/>
                <SidebarItem text="All" iconComponent={<BookmarksIcon/>} count={300}/>
                <SidebarItem text="Favorites" iconComponent={<FavoriteIcon/>} count={1}/>
                <SidebarItem text="Unsorted" iconComponent={<SortIcon/>} count={20}/>
                <SidebarItem text="Unread" iconComponent={<DraftsIcon/>} count={5}/>
              </List>
              <Divider/>
              <List className="drawer" disablePadding dense>
                <SidebarSubheader text="My Collections"/>
                <SidebarItem text="Web Development" count={20}/>
                <SidebarItem text="Politics" count={20}/>
              </List>
            </div>
          </div>
        </Drawer>
      </Hidden>
    </nav>
  );
}
