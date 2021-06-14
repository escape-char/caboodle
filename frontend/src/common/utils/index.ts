import qs from 'qs'
import {PUBLIC_URL} from '../../constants';

export function getFile(file:string): string{
  const f = file.startsWith("/") ? file.substring(1) : file;
  return `${PUBLIC_URL}/${f}`;
}
/**
 * 
 * @param obj object to get value from
 * @param path path of value  
 * @param defaultValue default value if path doesn't exist
 * @returns value at the given path
 */
export const get = (obj:Record<string, any>, path:Array<string>, defaultValue:any = undefined) => {
  const travel = (regexp:RegExp) =>
    String.prototype.split
      .call(path, regexp)
      .filter(Boolean)
      .reduce((res, key) => (res !== null && res !== undefined ? res[key] : res), obj);
  const result = travel(/[,[\]]+?/) || travel(/[,[\].]+?/);
  return result === undefined || result === obj ? defaultValue : result;
};

/**
 * check if variable if function
 * @param f variable to check if function
 * @returns  true if function
 */
export const isFunction = (f:any):boolean=>{
  return typeof f === 'function';
}

export const isString = (s:any):boolean=>{
  return typeof s === 'string';
}

export function setLocalStorage(key: string, data:any){
  localStorage.setItem(key, JSON.stringify(data))
}

export function getLocalStorage(key: string): any {
  const item: string | null = localStorage.getItem(key)
  return item && JSON.parse(item)
}

export function removeLocalStorage(key:string): void{
  localStorage.removeItem(key)
}

export function getURLParams(): Record<string, any>{
  const search: string = window.location.search.replace(/^\?/g, "")
  return qs.parse(search)
}
export function getURLPathWithParams(){
  return encodeURIComponent(window.location.pathname) + encodeURIComponent(window.location.search)
}
