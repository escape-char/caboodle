import React from 'react'
import Collapse from '@material-ui/core/Collapse'
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';
import Alert from '../../common/components/Alert'
import {useGlobalAlert} from './context'

export default function GlobalAlert(_:any){
  const {alert, removeAlert} = useGlobalAlert()

  return (
    <Collapse in={!!alert}>
      {alert &&
        <Alert 
          message={{
            title: alert.title,
            message: alert.message ,
            severity: alert.severity
          }}
          action={
              <IconButton
                aria-label="close"
                color="inherit"
                size="small"
                onClick={() => {
                  removeAlert()
                }}
            >
              <CloseIcon fontSize="inherit" />
            </IconButton>
          }
        />
      }

    </Collapse>
  )

}
