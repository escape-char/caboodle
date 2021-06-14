import React from 'react'
import {
  Alert as MAlert, 
  AlertTitle
} from '@material-ui/lab';

export enum AlertType {
  Error = "error",
  Info = "info",
  Warning = "warning",
  Success = "success"
}
export type AlertMessage = {
  title?: string,
  message: string,
  severity:  AlertType,
}

export type AlertProps = {
  message: AlertMessage,
  action: React.ReactNode
}

const titleLookup = {
  [AlertType.Error]: "Error",
  [AlertType.Info]: "Info",
  [AlertType.Warning]: "Warning",
  [AlertType.Success]: "Success"
}

const defaultProps = {severity: AlertType.Info}

function Alert(props: AlertProps){
  const {message, action} = props
  const title: string = message.title || titleLookup[message.severity]
  return ( 
    <MAlert severity={message.severity} action={action}>
      <AlertTitle>{title}</AlertTitle>
      {message.message}
    </MAlert>
  )
}

Alert.defaultProps = defaultProps
export default Alert
