import {AuthData, User} from '../../common/interfaces'
import * as authUtils from '../../common/utils/auth'
import {apiReq, HTTPMethod, HTTPContentType} from '../../common/request'

export class AuthService{
  authData: AuthData | null;
  user: User | null;

  constructor(){
    this.authData =  authUtils.getAuthData()
    this.user = authUtils.getUser()
  }
  updateUser(user:User){
    const user2: User = {...(this.user || {}), ...user}
    this.user = user2
    authUtils.setUser(user2)
  }
  updateAuthData(authData: AuthData){
    this.authData = authData
    authUtils.setAuthData(authData)
  }
  getUser(): User | null{
    return this.user
  }
  getToken(): string | null{
    const data:AuthData | null = authUtils.getAuthData()
    return data ? data.token : null
  }
  getAuthData(): AuthData | null{
    return authUtils.getAuthData()
  }
  isAuthenticated(): boolean{
    return authUtils.isAuthenticated()
  }
  async login(username:string, password: string){
    return apiReq({
      method: HTTPMethod.POST,
      endpoint: "/auth",
      data: {username, password},
      options: {
        headers: {"content-type": HTTPContentType.FORM_URL_ENCODED}
      },
      includeToken: false
    }).then((resp)=>{
      if(typeof(resp.data) !== "object"){
        throw new Error("invalid response data")
      }
      this.user = resp.data?.user
      this.authData = {token: resp.data?.token, expires_at: resp.data?.expires_at}
      authUtils.setUser(resp.data?.user)
      authUtils.setAuthData(this.authData)
      return Promise.resolve(resp)
    }).catch((data)=>{
      return Promise.reject(data)
    })
  }
  logout(redirect=true){
    this.authData = this.user = null
    authUtils.clearAuthData()
    authUtils.clearUser()
  }

}

const authService: AuthService = new AuthService()

export default authService
