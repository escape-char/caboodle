export enum InputType {
  BUTTON =  "button",
  CHECKBOX = "checkbox",
  COLOR = "color",
  DATE = "date",
  DATETIME_LOCAL = "datetime-local",
  EMAIL = "email",
  FILE = "file",
  HIDDEN = "hidden",
  IMAGE = "image",
  MONTH = "month",
  NUMBER = "number",
  PASSWORD = "password",
  RANGE = "range",
  SEARCH = "search",
  SUBMIT = "submit",
  TEL = "tel",
  TEXT = "text",
  TIME = "time",
  URL = "url",
  WEEK = "week"
}

export const API_URL: string | undefined = process.env.REACT_APP_CABOODLE_API_URL 

