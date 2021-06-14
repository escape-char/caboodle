import {STORAGE_SESSION_KEY, STORAGE_AUTH_KEY} from '../../constants'
import {getLocalStorage, setLocalStorage, removeLocalStorage} from './'
import type {User, AuthData} from '../interfaces'

export function getUser():User | null{
  return getLocalStorage(STORAGE_SESSION_KEY)
}

export function setUser(u: User){
  setLocalStorage(STORAGE_SESSION_KEY, u)
}

export function clearUser(){
  removeLocalStorage(STORAGE_SESSION_KEY)
}

export function getAuthData(): AuthData | null{
  return getLocalStorage(STORAGE_AUTH_KEY)
}
export function getToken(): string | null{
  const result: AuthData | null = getAuthData()
  return result ? result.token : null 

}

export function setAuthData(a: AuthData){
  return setLocalStorage(STORAGE_AUTH_KEY, a)
}

export function clearAuthData(){
  return removeLocalStorage(STORAGE_AUTH_KEY)
}

export function isAuthenticated(): boolean{
  const [user, authData] = [getUser(), getAuthData()]
  return !!(user?.username && authData?.token)
}
