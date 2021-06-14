import qs from 'qs'
import { API_URL } from "../constants"
import {getToken} from "./utils/auth"

export enum HTTPMethod{
  PUT = "PUT",
  GET = "GET",
  POST = "POST",
  PATCH  = "PATCH",
  OPTIONS = "OPTIONS",
  HEADERS = "HEADERS",
  DELETE = "DELETE"
}

export enum HTTPContentType{
  APPLICATION_JSON = "application/json",
  APPLICATION_JSON_UTF8 = "application/json; charset=utf-8",
  FORM_URL_ENCODED = "application/x-www-form-urlencoded",
  FORM_MULTI_PART = "multipart/form-data",
  TEXT_HTML = "text/html; charset=utf-8"
}


type ReqOptions = {
  mode?: RequestMode,
  cache?: RequestCache,
  credentials?: RequestCredentials | undefined, 
  headers?: Record<string, string>,
  redirect?: RequestRedirect,
  referrerPolicy?: ReferrerPolicy,
}

export function is_json(contentType: string | null): boolean{
  const s: string = contentType || ""
  return (
    s.toLowerCase() === HTTPContentType.APPLICATION_JSON_UTF8 ||
    s.toLowerCase() === HTTPContentType.APPLICATION_JSON
  )
}

export function is_url_encoded_form(contentType: string | null): boolean{
  return (contentType || "").toLowerCase() === HTTPContentType.FORM_URL_ENCODED
}


export function req(
  method: HTTPMethod,
  url: string,
  params?: Record<string, any>,
  data?: Record<string, any> | Array<Record<string, any>> | string | null,
  options?: ReqOptions
): Promise<Response>{
  const headers: Headers = new Headers((options?.headers || {}))

  if(!headers.has("content-type")){
    headers.set("content-type", HTTPContentType.APPLICATION_JSON_UTF8)
  }

  const contentType: string = headers.get("content-type") || ""

  let body: string | null | undefined; 

  //parse data based on the content type passed
  if(data){
    if(is_json(contentType)){
      body = JSON.stringify(data)
    }
    else if(is_url_encoded_form(contentType)){
      body = qs.stringify(data)
    }
  }else{
    if(Array.isArray(data) || typeof(data) === "object"){
      throw new Error("body contains invalid type object or array for given content-type")
    }
    body = data
  }

  const options2: RequestInit  = {
    method: method,
    headers: headers,
    body: body,
    mode: options?.mode,
    cache: options?.cache,
    credentials: options?.credentials,
    redirect: options?.redirect,
    referrerPolicy: options?.referrerPolicy
  }

  const full_url = params ? `${url}?${qs.stringify(params)}` : url

  return fetch(full_url, {
    method: method,
    ...options2
  })
}


type APIReqParams = {
  method: HTTPMethod,
  endpoint: string,
  params?: Record<string, any>,
  data?: Record<string, any> | Array<Record<string, any>> | string | null,
  options?: ReqOptions,
  includeToken?: boolean 

}

type APIResponse =  {
  data?: Record<string, any> | string | null,
  statusText?: string,
  status?: number,
  success: boolean,
  error?: string | null
}

export function _handleResponse(resp?: Response, error?: Error): Promise<APIResponse>{
  const UNKNOWN_ERROR: string = "An unknown error occured. Please try again"
  const NETWORK_ERROR: string = "Unable to communicate with remote API. This could mean the API is down or you're not connected to the internet"
  const getData = (resp:Response): Promise<Record<string, any> | string> =>{
    if(is_json(resp.headers.get("content-type"))){
      return resp.json()
    }else{
      return resp.text()
    }
  }
  const getError = (data: Record<string, any> | string | null): string=>{
    if(typeof(data) === "object" && data){
      return data.detail || data.message
    }
    else if(typeof(data) === "string"){
      return data
    }
    return UNKNOWN_ERROR
  } 

  return new Promise<APIResponse>((resolve, reject)=>{
    if(resp){
      getData(resp).then((data: Record<string, any> | string)=>{
        if(!resp.ok){
          reject({
            status: resp.status,
            statusText: resp.statusText,
            success:false,
            data: data,
            error: getError(data)
          })
        }
        else{
          resolve({
            status: resp.status,
            statusText: resp.statusText,
            success: true,
            data: data,
          })
        }
      })
    }else{
      //no response, network error
      reject({
        success: false,
        error: NETWORK_ERROR
      })
    }
  })

}
export function apiReq(
  {
    method,
    endpoint,
    params,
    data,
    options,
    includeToken = true
  }: APIReqParams
): Promise<APIResponse>{
  const headers: Record<string, string> = {
    "content-type": HTTPContentType.APPLICATION_JSON_UTF8,
    ...(options?.headers || {})
  }

  const parsedEndpoint = endpoint.startsWith("/") ? endpoint.substring(1) : endpoint

  const token: string | null = getToken()

  if(includeToken && token){
    headers["Authorization"] = `Bearer ${token}`
  }

  const options2 = {...(options || {}), headers}

  return req(
    method,
    `${API_URL}/${parsedEndpoint}`,
    params,
    data,
    options2
  ).then(resp =>{
    return _handleResponse(resp)
  }).catch((e)=>{
    return _handleResponse(undefined, e)
  })
}
