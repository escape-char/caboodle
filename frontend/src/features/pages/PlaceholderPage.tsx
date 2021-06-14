import Page, {PageHeader, PageContent} from './Page'

type PlaceholderPropsType = {
  title?: string,
  text?: string
}

const defaultProps = {
  title: "Coming Soon", 
  text: "This feature is coming soon. Please stand by for future updates."
}

function PlaceholderPage({title, text}: PlaceholderPropsType){

  return (
    <Page fixed>
      <PageHeader> {title} </PageHeader>
      <PageContent>
        <p>{text}</p>
      </PageContent>
    </Page>
  )

}

PlaceholderPage.defaultProps = defaultProps
export default PlaceholderPage
