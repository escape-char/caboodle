
/**
 * Form which uses for react hook forms for easier validation and management
 */
import React from 'react';
import {ResolverResult, FormProvider, useForm}  from 'react-hook-form';
import List, {ListProps} from '@material-ui/core/List';
import {makeStyles} from '@material-ui/core/styles';
import ListItem  from '@material-ui/core/ListItem';
import Container from '../layouts/Container';


/**
 * properties for form
 */
export interface FormProps {
  defaultValues?: Record<string, any>
  //callback for onSubmit event
  onSubmit(values:Record<string, any>): void
  //resolver for validation; typically used for yup schema validation
  resolver?(values: any, context?: object): Promise<ResolverResult> | ResolverResult ,

  disableGutters?:boolean,

  //children of the form
  children: any
}

const defaultProps = {
  disableGutters: false
}

/**
 * Form which uses react hook form
 * @param props  properties for form
 * @returns  form as react element
 */
function Form(props:FormProps):React.ReactElement{
  const {
    resolver, 
    disableGutters,
    onSubmit, 
    children, 
    defaultValues
  } = props;
  const methods = useForm({mode: 'onBlur', resolver, defaultValues})

  return (
    <Container disableGutters={disableGutters}>
      <FormProvider {...methods}>
        <form onSubmit={methods.handleSubmit(onSubmit)} noValidate>
          {children}
        </form>
      </FormProvider>
    </Container>
  )
}


const useFooterStyles = makeStyles({
  "formFooter":{
    'display': 'inline-block',
    "width": '100%'
  },
  "formFooterItem":{
    "paddingLeft": "0px",
    "paddingRight": "0px"
  }
})

export type FormFooterProps = ListProps & {
  inline?:boolean
};

export function FormFooter(props:FormFooterProps):React.ReactElement{
  const classes = useFooterStyles();
  return (
    <List className={props.inline ? classes.formFooter: undefined} {...props}/>
  );

}

export function FormFooterItem(props:any){
  const classes = useFooterStyles();
  return <ListItem className={classes.formFooterItem} {...props}/>
}

Form.defaultProps = defaultProps;

export default Form;
