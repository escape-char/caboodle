import {PUBLIC_URL} from '../constants';

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
