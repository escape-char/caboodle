
export const PUBLIC_URL:string=process.env.PUBLIC_URL
export const API_URL:string|undefined=process.env.REACT_APP_CABOODLE_API_URL
export const STORAGE_SESSION_KEY="__caboodle_session__"
export const STORAGE_AUTH_KEY="__caboodle_auth__"


export enum AsyncStatus {
  Idle = 'idle',
  Pending = "pending",
  Error = 'rejected',
  Success = "resolved"
}
