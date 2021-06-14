import React, {
  createContext, 
  useState, 
  useContext,
  useCallback 
} from 'react';
import {AlertMessage} from '../../common/components/Alert'


type GlobalAlertContextType = {
  alert: AlertMessage | null,
  addAlert:  Function,
  removeAlert: Function
}

export const GlobalAlertContext = createContext<GlobalAlertContextType>({
  alert:null, 
  addAlert: ()=>{},
  removeAlert: ()=>{}
})

export default function GlobalAlertProvider({children}: {children: React.ReactNode}){
  const [alert, setAlert]= useState<AlertMessage | null>(null)

  const removeAlert = ()=>setAlert(null)
  const addAlert = (a:AlertMessage)=>{
    setAlert(a)
  }

  const contextValue =  {
    alert,
    addAlert: useCallback((a: AlertMessage) => addAlert(a), []),
    removeAlert: useCallback(() => removeAlert(), [])
  }

  return (
    <GlobalAlertContext.Provider value={contextValue}>
      {children}
    </GlobalAlertContext.Provider>
  )
}

export function useGlobalAlert(){
  const {alert, addAlert, removeAlert} = useContext(GlobalAlertContext)
  return {alert, addAlert, removeAlert}
}
