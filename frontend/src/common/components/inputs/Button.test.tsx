/**
 * tests for Button UI component
 */
import React from 'react';
import { render } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Button, {ButtonSize, ButtonColor, ButtonVariant} from './Button';

const BTN_TEXT = "Submit";

test('test rendering of button', () => {
  
  const {getByText} = render(<Button>{BTN_TEXT}</Button>);

  const elem:HTMLElement = getByText(BTN_TEXT);

  //test submit button is in document
  expect(elem).toBeInTheDocument();
  expect(elem.closest('button')).toBeEnabled();

});

test('test click button', () => {
  const handleClick = jest.fn();
  
  const {getByText} = render(<Button onClick={handleClick}>{BTN_TEXT}</Button>);

  const elem:HTMLElement = getByText(BTN_TEXT);

  //test click callback method is called
  userEvent.click(elem);

  expect(handleClick).toHaveBeenCalledTimes(1)
});


test('test rendering of loading button', () => {
  const handleClick = jest.fn();
  const {getByRole} = render(<Button onClick={handleClick} loading>{BTN_TEXT}</Button>);
  const elem:HTMLElement = getByRole("progressbar");
});

test('test rendering of disabled button', ()=>{
  const {getByText} = render(<Button disabled>{BTN_TEXT}</Button>);
  expect(getByText(BTN_TEXT).closest('button')).toBeDisabled();
});


test('test rendering of small button', ()=>{
  const {getByText} = render(<Button size={ButtonSize.SMALL}>{BTN_TEXT}</Button>);
  expect(getByText(BTN_TEXT).closest('button')).toHaveClass("MuiButton-sizeSmall");
});

test('test rendering of large button', ()=>{
  const {getByText} = render(<Button size={ButtonSize.LARGE}>{BTN_TEXT}</Button>);
  expect(getByText(BTN_TEXT).closest('button')).toHaveClass("MuiButton-sizeLarge");
});


test('test rendering of large button', ()=>{
  const {getByText} = render(<Button size={ButtonSize.LARGE}>{BTN_TEXT}</Button>);
  expect(getByText(BTN_TEXT).closest('button')).toHaveClass("MuiButton-sizeLarge");
});

test('test rendering of primary color', ()=>{
  const {getByText} = render(<Button color={ButtonColor.PRIMARY}>{BTN_TEXT}</Button>);
  expect(getByText(BTN_TEXT).closest('button')).toHaveClass("MuiButton-textPrimary");
});

test('test rendering of secondary color', ()=>{
  const {getByText} = render(<Button color={ButtonColor.SECONDARY}>{BTN_TEXT}</Button>);
  expect(getByText(BTN_TEXT).closest('button')).toHaveClass("MuiButton-textSecondary");
});


test('test rendering of contained button', ()=>{
  const {getByText} = render(<Button variant={ButtonVariant.CONTAINED}>{BTN_TEXT}</Button>);
  expect(getByText(BTN_TEXT).closest('button')).toHaveClass("MuiButton-contained");
});

test('test rendering of outlined button', ()=>{
  const {getByText} = render(<Button variant={ButtonVariant.OUTLINED}>{BTN_TEXT}</Button>);
  expect(getByText(BTN_TEXT).closest('button')).toHaveClass("MuiButton-outlined");
});

test('test rendering of text button', ()=>{
  const {getByText} = render(<Button variant={ButtonVariant.TEXT}>{BTN_TEXT}</Button>);
  expect(getByText(BTN_TEXT).closest('button')).toHaveClass("MuiButton-text");
});


