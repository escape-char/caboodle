/**
 * UI component for Button
 */

import React from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';
import {makeStyles} from '@material-ui/core/styles';
import {default as MButton, ButtonProps as MButtonProps} from '@material-ui/core/Button';

/**
 * Types of buttons
 */
export enum ButtonVariant {
  //buttons are filled and raised
  CONTAINED = "contained",
  // button contains only text
  TEXT =  "text",
  //button raised but no fill color
  OUTLINED = "outlined"
}

/**
 * Colors for button
 */
export enum ButtonColor {
  //primary color
  PRIMARY = "primary",
  //secondary color
  SECONDARY = "secondary",
  //default color
  DEFAULT = "default",
  //inherit the color from theme
  INHERIT = "inherit"
}

/**
 * Button sizes
 */
export enum ButtonSize {
  SMALL = "small",
  MEDIUM = "medium",
  LARGE = "large"
}

/**
 * Button properties
 */
export type ButtonProps = MButtonProps & {
  loading?: boolean //whether to display loading indicator
};

/**
 * default properties
 */
const defaultProps = {
  loading: false,
  disabled:false
};

/**
 * Styles for button
 */
const useStyles = makeStyles((theme) => ({
  //style for loading indicator
  buttonProgress: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    marginTop: -12,
    marginLeft: -12,
  },
}));

/**
 * UI Button
 * @param props properties for UI button
 * @returns button as react element
 */
function  Button(props: ButtonProps): React.ReactElement{
  const {loading, ...bProps} = props;
  const classes = useStyles();

  return (
    <React.Fragment>
      <MButton role="button" {...bProps} />
      {loading && <CircularProgress size={24} className={classes.buttonProgress} />}
    </React.Fragment>
  );

};

Button.defaultProps = defaultProps;

export default Button;
