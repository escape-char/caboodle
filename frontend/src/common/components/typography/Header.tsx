/**
 * Headers for UI
 */
import React from 'react';
import Typography, {TypographyProps} from '@material-ui/core/Typography';
import {makeStyles} from '@material-ui/core/styles';

/**
 * properties for header
 */
export type HeaderProps = TypographyProps & {useDark?: boolean};


const useStyles = makeStyles((theme)=>{
  return {
    light: {
      color:theme.palette.grey[50]
    }
  }
}); 

/**
 * Headers for UI
 * @param props properties for header
 * @returns  headers as react element
 */
export default function Header(props: HeaderProps): React.ReactElement{
  const {useDark, ...props2} = props;
  const classes = useStyles(props);
  return <Typography className={useDark ? classes.light : undefined} {...props2}/>
}

