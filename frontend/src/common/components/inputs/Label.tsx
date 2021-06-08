/**
 * UI label for inputs 
 */

import React from 'react';
import {default as InputLabel, InputLabelProps} from '@material-ui/core/InputLabel'
import {makeStyles} from '@material-ui/core/styles';

const useStyles = makeStyles((theme)=>{
  return {
    "label":{
      top: "-5px",
      transform: "none",
    }
  };
})
/**
 * propertes for label using Material UI props
 */
export type LabelProps = InputLabelProps;

/**
 * UI label for inputs
 * @param props  Label properties to be passed in
 * @returns label as react element
 */
export default function Label(props: LabelProps): React.ReactElement{
  const classes = useStyles();
  return (<InputLabel className={classes.label} {...props}/>);
}
