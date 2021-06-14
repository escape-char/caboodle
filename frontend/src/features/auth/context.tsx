import React from 'react'
import {useAsync, defaultInitialState} from '../../common/hooks/useAsync'
import {User, AuthData} from '../../common/interfaces'
import authService from './service'
import {useGlobalAlert} from '../globalalert/context'
import { AlertType } from '../../common/components/Alert'


type AuthContextType = {
  user: User | null,
  authData: AuthData | null,
  login: Function, 
  logout: Function,
  isAuthenticated: Function
}
const AuthContext = React.createContext<AuthContextType>({
  user: null,
  authData: null,
  login: ()=>{},
  logout: ()=>{},
  isAuthenticated: ()=>{}
})
AuthContext.displayName = 'AuthContext'

type AuthResponse = {user: User, token:string, expires_at: string}

function AuthProvider(props: object) {
  const {
    data,
    setData,
  } = useAsync(defaultInitialState)
  const authData: AuthResponse = data as AuthResponse
  const {addAlert, removeAlert} = useGlobalAlert()


  const login = React.useCallback(
    (username:string, password:string) => {
      return authService.login(username, password).then(
        data => {
          console.log('inside then of login context')
          setData(data)
          removeAlert()
      }).catch((resp =>{
        console.log("error in catch: ", resp)
        addAlert({title: "Error", message: resp.error, severity: AlertType.Error})
      }))
    },
    [setData, addAlert, removeAlert],
  )
  const logout = React.useCallback(() => {
    authService.logout()
    setData(null)
  }, [setData])

  const isAuthenticated = React.useCallback(() => {
   return authService.isAuthenticated()
  }, [])


  const value = React.useMemo(
    () => ({
      user: authData?.user, 
      authData: {token: authData?.token, expires_at: authData?.expires_at}, 
      login, 
      logout, 
      isAuthenticated
      }),
      [login, logout, isAuthenticated, authData],
  )

  return <AuthContext.Provider value={value} {...props} />

}

function useAuth() {
  const context = React.useContext(AuthContext)
  if (context === undefined) {
    throw new Error(`useAuth must be used within a AuthProvider`)
  }
  return context
}

/*
TODO: FIXME
function useClient() {
  const {user} = useAuth()
  const token = user?.token
  return React.useCallback(
    (endpoint, config) => client(endpoint, {...config, token}),
    [token],
  )
}
*/


export {AuthProvider, useAuth}
