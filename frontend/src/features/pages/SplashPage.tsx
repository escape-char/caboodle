/**
 * Splash Page UI
 * 
 * splash pages contains a splash image on the right and information/input on the left
 */
import React from "react";
import { Grid } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import Page, {PageHeader, PageContent, PageSubheader} from './Page';
import {isString} from '../../common/utils';
import GlobalAlert from '../globalalert/GlobalAlert'

/**
 * Splash page properties
 */
export interface SplashPageProps {
  //classes for the content page
  classes?: object;
  //max width of the content page
  maxWidth?: false | "xs" | "sm" | "md" | "lg" | "xl" | undefined;
  //children of the content page
  children: React.ReactChild | React.ReactFragment | React.ReactPortal,
  //header for the content page
  header: string | React.ReactNode,
  //sub header fo rthe content page
  subheader?: string | React.ReactNode

  splashHeader: string | React.ReactNode,
  splashSubheader: string | React.ReactNode,
  splashContent: Function 
}


/**
 * Styles for splash page
 */
const useStyles: Function = makeStyles((theme)=>{
  return {
    root: {
      height: "100%",
      width: "100%",
      flexGrow: 1,
    },
    splash: {
      background: theme.palette.primary.main,
    },
    page:{
      padding: theme.spacing(16),
    },
  }
});

/**
 * Splash page UI
 * 
 * display splash image on the right and page content on the left
 * @param props properties for splash page
 * @returns splash page as react element
 */
export default function SplashPage(props: SplashPageProps): React.ReactElement {
  const classes: Record<string, string> = useStyles(props);
  const {splashContent} = props;

  return (
    <Grid className={classes.root} container>
      <Grid item sm={12} md={5}>
        <Page className={classes.page}>
          <GlobalAlert/>
          <PageHeader> {props.header} </PageHeader>
          <PageSubheader> {props.subheader} </PageSubheader>
          <PageContent disableGutters>
            {props.children}
          </PageContent>
        </Page>
      </Grid>
      <Grid sm={12} md={7} className={classes.splash} item>
        <Page className={classes.page}>
          <PageHeader useDark> {props.splashHeader}</PageHeader>
          <PageSubheader> {props.splashSubheader}</PageSubheader>
          <PageContent disableGutters useDark>
            {!isString(props.splashContent) && (splashContent(props) as Function)}
          </PageContent>
        </Page>
      </Grid>
    </Grid>
  );
}

