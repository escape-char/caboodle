import { RouteComponentProps } from 'react-router-dom';
import { SplashPage } from '../common/components/pages';
import {Form, FormInput, FormFooter, FormFooterItem} from '../common/components/forms';
import { InputType } from '../common/components/inputs/constants';
import {default as Button, ButtonSize, ButtonVariant, ButtonColor} from '../common/components/inputs/Button';

export default function SignIn(props: RouteComponentProps): React.ReactElement{
    return (
      <SplashPage 
          header="Sign In"
          subheader="Sign in to begin managing your bookmarks"
          splashHeader="Welcome to Caboodle"
          splashSubheader="Where we meet all your bookmarking needs"
          splashContent={()=>{
            return (
              <>
                <p>You are just a few seconds away from managing your bookmarks. 
                  You will need to sign up for an account or sign in with an existing account to continue
                </p>
                <Button 
                  variant={ButtonVariant.CONTAINED} 
                  color={ButtonColor.SECONDARY} 
                  size={ButtonSize.LARGE}
                >
                    Sign Up
                </Button>
              </>

            );
          }}
        >
        <Form onSubmit={(values)=>{
        }} disableGutters>
          <FormInput 
            label="Username" 
            name="username" 
            rules={{required:true}}
            placeholder="Enter username..."
            required
            inputProps={{fullWidth:true}}/>
          <FormInput 
            label="Password" 
            name="password" 
            placeholder="Enter password..."
            type={InputType.PASSWORD}
            inputProps={{fullWidth:true}}/>

          <FormFooter>
            <FormFooterItem>
              <Button fullWidth={true} variant={ButtonVariant.CONTAINED} color={ButtonColor.PRIMARY}>Sign In</Button>
            </FormFooterItem>
            <FormFooterItem>
              <Button fullWidth={true} size={ButtonSize.SMALL}>Forgot Your Password?</Button>
            </FormFooterItem>
            <FormFooterItem>
              <Button fullWidth={true} size={ButtonSize.SMALL}>Don't Have an Account?</Button>
            </FormFooterItem>
          </FormFooter>
        </Form>
      </SplashPage>
    );
}
