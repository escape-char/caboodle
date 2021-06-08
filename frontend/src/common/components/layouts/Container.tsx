/**
 * UI container for holding components
 */

import React from 'react';
import {default as MContainer, ContainerProps as MContainerProps} from '@material-ui/core/Container';
import {makeStyles} from '@material-ui/core/styles'

const useStyles = makeStyles((theme)=>{
  return {
    'light': {
      color:  theme.palette.grey[50]
    }
  };

});


/**
 * containers properties
 */
export type ContainerProps = MContainerProps & {useDark?:boolean};

/**
 * Container for holding components
 * @param props  container properties
 * @returns  container as react element
 */
export default function Container(props: ContainerProps) :React.ReactElement{
  const {useDark, ...props2} = props;
  const classes = useStyles();

  return (
    <MContainer className={useDark? classes.light : undefined} {...props2}/>
  );
}

