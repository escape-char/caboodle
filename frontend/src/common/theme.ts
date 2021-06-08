import { ThemeOptions } from "@material-ui/core/styles";
import { lighten, darken } from "./utils/theme";

//theme colors
export const BLEACHED_CEDAR_PURPLE: string = "#0C121D";
export const BRADY_PUNCH_YELLOW: string = "#c5771d";
export const CARARRA_WHITE: string = "#F4F6F3";
export const DAISY_BUSH_BLUE: string = "#0F0E6C";
export const HIPPIE_PINK: string = "#AF4859";
export const POMEGRANATE_RED: string = "#f44335";
export const SHIP_COVE_BLUE: string = "#7489B9";
export const VIRIDIAN_GREEN: string = "#488764";
export const GRAY: string = "#999998";

export const PRIMARY_COLOR_MAIN: string = BLEACHED_CEDAR_PURPLE;
export const PRIMARY_COLOR_LIGHT: string = lighten(PRIMARY_COLOR_MAIN, 15);
export const PRIMARY_COLOR_DARK: string = darken(PRIMARY_COLOR_MAIN, 15);

export const SECONDARY_COLOR_MAIN: string = HIPPIE_PINK;
export const SECONDARY_COLOR_LIGHT: string = lighten(SECONDARY_COLOR_MAIN, 15);
export const SECONDARY_COLOR_DARK: string = darken(SECONDARY_COLOR_MAIN, 15);

export const BACKGROUND_LIGHT: string = CARARRA_WHITE;
export const BACKGROUND_DARK: string = BLEACHED_CEDAR_PURPLE;

export const SUCCESS_MAIN: string = VIRIDIAN_GREEN;
export const SUCCESS_LIGHT: string = lighten(SUCCESS_MAIN, 15);
export const SUCCESS_DARK: string = darken(SUCCESS_MAIN, 15);

export const ERROR_MAIN: string = POMEGRANATE_RED;
export const ERROR_LIGHT: string = lighten(POMEGRANATE_RED, 15);
export const ERROR_DARK: string = darken(POMEGRANATE_RED, 15);


export const WARNING_MAIN: string = BRADY_PUNCH_YELLOW;
export const WARNING_LIGHT: string = lighten(BRADY_PUNCH_YELLOW, 15);
export const WARNING_DARK: string = darken(BRADY_PUNCH_YELLOW, 15);

export const INFO_MAIN: string = BLEACHED_CEDAR_PURPLE;
export const INFO_LIGHT: string = lighten(BLEACHED_CEDAR_PURPLE, 15);
export const INFO_DARK: string = darken(BLEACHED_CEDAR_PURPLE, 15);

export const APP_BAR_HEIGHT:number = 48;

const defaultTheme: ThemeOptions = {
  palette: {
    primary: {
      main: PRIMARY_COLOR_MAIN,
      dark: PRIMARY_COLOR_DARK,
      light: PRIMARY_COLOR_LIGHT,
    },
    secondary: {
      main: SECONDARY_COLOR_MAIN,
      dark: SECONDARY_COLOR_DARK,
      light: SECONDARY_COLOR_LIGHT,
    },
    success: {
      main: SUCCESS_MAIN,
      dark: SUCCESS_DARK,
      light: SUCCESS_LIGHT,
    },
    warning: {
      main: WARNING_MAIN,
      dark: WARNING_DARK,
      light: WARNING_LIGHT,
    },
    error: {
      main: ERROR_MAIN,
      dark: ERROR_DARK,
      light: ERROR_LIGHT,
    },
    background: {
      default: BACKGROUND_LIGHT,
    },
    text: {
      primary: PRIMARY_COLOR_MAIN,
    },
  },
};
export default defaultTheme;
