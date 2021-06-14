import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import {Header} from '../../common/components/typography';

const useStyles = makeStyles((theme)=>{
  return {
    title: {
      display: 'none',
      [theme.breakpoints.up('sm')]: {
        display: 'block',
      },
    }
  };
});

export type AppBarHeaderProps = {header: string};

export default function AppBarHeader(props: AppBarHeaderProps): React.ReactElement{
  const classes = useStyles();
  return <Header className={classes.title} variant="h6" noWrap>{props.header}</Header>
}
