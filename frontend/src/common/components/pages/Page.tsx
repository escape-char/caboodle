import React from "react";
import Container, {ContainerProps} from "../layouts/Container";
import {default as Header, HeaderProps} from '../typography/Header';

export type PageProps = ContainerProps;

export default function Page(props: PageProps) {
  return (
    <Container {...props}/>
  );
}

export function PageHeader(props: HeaderProps){
  return (<Header {...props} variant="h3" gutterBottom/> );
}
export function PageSubheader(props: HeaderProps){
  return (<Header {...props} variant="subtitle1" gutterBottom color="secondary"/> );
}

export function PageContent(props: ContainerProps){
  return (<Container {...props}/>);
}


