import React from 'react';
import { WorkflowSchema } from './types';
import StyledBooleanInput, { IBooleanProps } from '../inputs/BooleanInput';
import StyledSelectInput, { ISelectProps } from '../inputs/SelectInput';
import StyledTextInput, { ITextProps } from '../inputs/TextInput';
import StyledFileInput from '../inputs/FileInput';
import StyledNumInput, { INumProps } from '../inputs/NumInput';

// -----------------------------------------------------------------------------
// Boolean input mapping
// -----------------------------------------------------------------------------
export const mapSchemaToBooleanInput = (
  id: string,
  schema: WorkflowSchema
): IBooleanProps => ({
  id: id,
  label: id,
  format: schema.format || '',
  description: schema.description || schema.help_text,
  defaultValue: schema.default
});

export const isBooleanInput = (schema: WorkflowSchema): boolean =>
  schema.type === 'boolean' ? true : false;

// -----------------------------------------------------------------------------
// File input mapping
// -----------------------------------------------------------------------------
export const isFileInput = (schema: WorkflowSchema): boolean =>
  schema.type === 'string' &&
  ['file-path', 'directory-path', 'path'].includes(schema.format)
    ? true
    : false;

// -----------------------------------------------------------------------------
// Num input mapping
// -----------------------------------------------------------------------------
export const mapSchemaToNumInput = (
  id: string,
  schema: WorkflowSchema
): INumProps => ({
  id: id,
  label: id,
  format: schema.format || '',
  description: schema.description || schema.help_text,
  defaultValue: schema.default,
  min: schema.minimum,
  max: schema.maximum
});

export const isNumInput = (schema: WorkflowSchema): boolean =>
  ['integer', 'number'].includes(schema.type) ? true : false;

// -----------------------------------------------------------------------------
// Select input mapping
// -----------------------------------------------------------------------------
export const mapSchemaToSelectInput = (
  id: string,
  schema: WorkflowSchema
): ISelectProps => ({
  id: id,
  label: id,
  format: schema.format || '',
  description: schema.description || schema.help_text,
  defaultValue: schema.default,
  choices: (schema.enum as string[]).map(Item => ({ value: Item, label: Item }))
});

export const isSelectInput = (schema: WorkflowSchema): boolean =>
  schema.enum ? true : false;

// -----------------------------------------------------------------------------
// Text input mapping
// -----------------------------------------------------------------------------
export const mapSchemaToTextInput = (
  id: string,
  schema: WorkflowSchema
): ITextProps => ({
  id: id,
  label: id,
  format: schema.format || '',
  description: schema.description || schema.help_text,
  defaultValue: schema.default
});

export const isTextInput = (schema: WorkflowSchema): boolean =>
  schema.type === 'string' && !schema.enum ? true : false;

// -----------------------------------------------------------------------------
// Input component mapper
// -----------------------------------------------------------------------------
export const getInputComponent = (
  id: string,
  schema: WorkflowSchema,
  error: string[],
  onChange: CallableFunction
): JSX.Element => {
  if (isBooleanInput(schema)) {
    return (
      <StyledBooleanInput
        {...mapSchemaToBooleanInput(id, schema)}
        error={error}
        onChange={onChange}
      />
    );
  } else if (isSelectInput(schema)) {
    return (
      <StyledSelectInput
        {...mapSchemaToSelectInput(id, schema)}
        error={error}
        onChange={onChange}
      />
    );
  } else if (isFileInput(schema)) {
    return (
      <StyledFileInput
        {...mapSchemaToTextInput(id, schema)}
        error={error}
        onChange={onChange}
      />
    );
  } else if (isTextInput(schema)) {
    return (
      <StyledTextInput
        {...mapSchemaToTextInput(id, schema)}
        error={error}
        onChange={onChange}
      />
    );
  } else if (isNumInput(schema)) {
    return (
      <StyledNumInput
        {...mapSchemaToNumInput(id, schema)}
        error={error}
        onChange={onChange}
      />
    );
  } else {
    return (
      <StyledTextInput
        {...mapSchemaToTextInput(id, schema)}
        error={error}
        onChange={onChange}
      />
    );
  }
};
