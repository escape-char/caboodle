/**
 * Input to be used in forms which uses react hook forms
 */
import React from "react";
import {useFormContext, Controller, RegisterOptions} from "react-hook-form";
import {default as Input, InputProps} from '../inputs/Input';

/**
 * Properties for input
 */
type FormInputProps = InputProps & { name: string, rules?:RegisterOptions};

/**
 * default properties
 */
const defaultProps = {
  name: ""
};

/**
 * Input to be used with react hook form
 * @param props  properties for input
 * @returns  input as react element
 */
function FormInput(props: FormInputProps): React.ReactElement {
  const {control, errors} = useFormContext();
  const { name, label, defaultValue, inputProps, labelProps, rules} = props;

  return (
    <Controller
      name={name}
      label={label}
      defaultValue={defaultValue}
      control={control}
      rules={rules}
      render={(
        field,
        fieldState
      ) => {
        const TYPE_REQUIRED = "required"
        const {onBlur, onChange, ref, name, value} = field;
        //For some reason, react hook type definition doesn't include error
        //so we have to typecast to include it
        const {invalid, isDirty} = fieldState;
        const showError:boolean = invalid && isDirty;
        const errorMessage = !errors[name] ? "" : 
          errors[name].type === TYPE_REQUIRED ? "this field is required" : errors[name]

        return (
          <Input 
            name={name}
            label={label}
            error={showError}
            type={props.type}
            required={props.required}
            disabled={props.disabled}
            placeholder={props.placeholder}
            onChange={onChange}
            onBlur={onBlur}
            defaultValue={value}
            helperText = {showError ? errorMessage : undefined}
            inputProps={{...inputProps, inputRef: ref}}
            labelProps={labelProps}
          />
        );
      }}
    />
  );
}

FormInput.defaultProps = defaultProps;

export default FormInput;
