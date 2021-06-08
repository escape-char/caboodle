/**
 * tests for Label UI input
 */

import React from 'react';
import { render } from '@testing-library/react';
import Label from './Label';

const LABEL_TEXT = "labeltext";

test('test rendering of label', () => {
  
  const {getByText} = render(<Label>{LABEL_TEXT}</Label>);

  const elem:HTMLElement = getByText(LABEL_TEXT);

  //test submit button is in document
  expect(elem).toBeInTheDocument();
  expect(elem.closest('label')).toBeEnabled();
});

test('test rendering of disabled label', () => {
  
  const {getByText} = render(<Label disabled>{LABEL_TEXT}</Label>);

  const elem:HTMLElement = getByText(LABEL_TEXT);

  expect(elem.closest('label')).toHaveClass("Mui-disabled");
});

test('test rendering of required label', () => {
  
  const {getByText} = render(<Label required>{LABEL_TEXT}</Label>);

  const elem:HTMLElement = getByText(LABEL_TEXT);

  expect(elem.closest('label')).toHaveClass("Mui-required");
  //check required asterick is rendered
  expect(getByText("*")).toBeInTheDocument();
});

test('test rendering of error label', () => {
  
  const {getByText} = render(<Label error>{LABEL_TEXT}</Label>);

  const elem:HTMLElement = getByText(LABEL_TEXT);

  expect(elem.closest('label')).toHaveClass("Mui-error");
});

