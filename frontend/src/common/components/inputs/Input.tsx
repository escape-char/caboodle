/**
 * UI commponent for input text field
 */

import React, {useState} from "react";
import {default as MInput, InputProps as MInputProps} from "@material-ui/core/Input";
import {default as FormControl, FormControlProps} from '@material-ui/core/FormControl';
import {default as FormHelperText, FormHelperTextProps} from '@material-ui/core/FormHelperText';
import {makeStyles} from '@material-ui/core/styles';
import {default as Label, LabelProps} from './Label';
import {InputType} from './constants';
import {lighten} from '../../utils/theme';
import {GRAY} from '../../theme';

const useStyles = makeStyles((theme)=>{
  return {
    'inputContainer': {
      "background": lighten(theme.palette.background.default, 10),
      "border": `1px solid ${GRAY}`
    },
    'input': {
      padding: theme.spacing(1)
    },

  }
})


/**
 * React properties for Input
 */
export interface InputProps{
  //name of input
  name: string,
  //label for input
  label?:string | React.ReactElement,
  //type of input; i.e. text, email
  type?: InputType,
  //placeholder for input when blank
  placeholder?: string,
  //whether input is disabled
  disabled?: boolean,
  //whether input has an error
  error?: boolean,
  defaultValue?: string,
  //whether input is required
  required?:boolean,
  fullWidth?: boolean,

  //helper text for input; used for displaying error message
  helperText?: string,
  //callback for onChange event
  onChange?(event:object): void,
  //callback for onBlue event
  onBlur?(event:object): void,
  //properties for the FormControl component
  formControlProps?: FormControlProps,
  //properties for the FormHelperText component
  formHelperTextProps?: FormHelperTextProps,
  //properties for the label component
  labelProps?: LabelProps,
  //properties for the input component
  inputProps?: MInputProps
}

/**
 * default properties
 */
const defaultProps = {
  placeholder: "Enter text...",
  inputProps: {},
  formControlProps: {margin: "normal"},
  type: InputType.TEXT,
  labelProps: {disableAnimation: true},
  formHelperTextProps: {},
  error: false,
  required: false,
  disabled: false,
  fullWidth: false
}

/**
 * UI input
 * @param props  properties for UI input
 * @returns  UI input as react element
 */
function Input(props: InputProps): React.ReactElement{
  const [value, setValue] = useState("");
  const {
    formControlProps, 
    inputProps, 
    name, 
    label, 
    helperText,
    placeholder
  } = props;

  const iProps = {
    ...inputProps, 
    defaultValue: props.defaultValue,
    placeholder: placeholder,
    required: props.required,
    disabled: props.disabled,
    type: props.type,
    error: props.error,
    onChange: props.onChange,
    onBlur: props.onBlur
  };

  const classes = useStyles();

  return (
    <FormControl role="group" {...formControlProps} error={props.error} disabled={props.disabled} fullWidth>
      {(label && props.labelProps) &&
        <Label 
          role="label"
          {...props.labelProps} 
          disabled={props.disabled}
          required={props.required}
          error={!!props.error}
        >
          {label}
        </Label>
      }

      <MInput 
        className={classes.inputContainer}
        {...iProps}
        inputProps={{role:"input", className:classes.input}}
        name={name} 
        onChange={(e)=>{
          setValue(e.target.value);
          iProps.onChange && iProps.onChange(e);
        }}
        onBlur={(e)=>{
          setValue(e.target.value);
          iProps.onBlur && iProps.onBlur(e);
        }}
        value={value}
      />
      {helperText &&
        <FormHelperText role="alert" error={!!props.error}>
          {props.helperText}
        </FormHelperText>
      }
    </FormControl>

  );
}

Input.defaultProps = defaultProps;

export default Input;
